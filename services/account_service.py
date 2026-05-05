"""
SOAP Service: AccountService
Endpoint: /account
Operations: GetAccountBalance
"""
from flask import Blueprint, request, Response
import xml.etree.ElementTree as ET
from data.mock_data import ACCOUNTS, TRANSACTIONS

account_bp = Blueprint("account", __name__)

TNS = "http://paritybank.com/account"
SOAP_NS = "http://schemas.xmlsoap.org/soap/envelope/"


def soap_envelope(body_xml: str) -> Response:
    xml = f"""<?xml version='1.0' encoding='UTF-8'?>
<soap11env:Envelope
  xmlns:soap11env="{SOAP_NS}"
  xmlns:tns="{TNS}">
  <soap11env:Body>
    {body_xml}
  </soap11env:Body>
</soap11env:Envelope>"""
    return Response(xml, mimetype="text/xml")


def soap_fault(message: str) -> Response:
    return soap_envelope(f"""
    <soap11env:Fault xmlns:soap11env="{SOAP_NS}">
      <faultcode>Server</faultcode>
      <faultstring>{message}</faultstring>
    </soap11env:Fault>""")


@account_bp.route("", methods=["GET", "POST"])
def handle():
    if request.method == "GET":
        return Response(WSDL, mimetype="text/xml")

    root = ET.fromstring(request.data)
    body = root.find(f"{{{SOAP_NS}}}Body")
    if body is None:
        return soap_fault("Missing SOAP Body"), 400

    op = next(iter(body), None)
    if op is None:
        return soap_fault("Empty SOAP Body"), 400

    local = op.tag.split("}")[-1] if "}" in op.tag else op.tag

    if local == "GetAccountBalance":
        account_id = op.findtext(f"{{{TNS}}}account_id") or ""
        account = ACCOUNTS.get(account_id)
        if not account:
            return soap_fault(f"Account not found: {account_id}"), 404

        txns = TRANSACTIONS.get(account_id, [])
        last = txns[0] if txns else {}

        return soap_envelope(f"""
    <tns:GetAccountBalanceResponse>
      <tns:GetAccountBalanceResult>
        <tns:account_id>{account["account_id"]}</tns:account_id>
        <tns:balance>{account["balance"]}</tns:balance>
        <tns:currency>{account["currency"]}</tns:currency>
        <tns:account_type>{account["account_type"]}</tns:account_type>
        <tns:status>{account["status"]}</tns:status>
        <tns:owner_name>{account["owner_name"]}</tns:owner_name>
        <tns:last_transaction_id>{last.get("id", "")}</tns:last_transaction_id>
        <tns:last_transaction_amount>{last.get("amount", "")}</tns:last_transaction_amount>
        <tns:last_transaction_date>{last.get("date", "")}</tns:last_transaction_date>
        <tns:last_transaction_description>{last.get("description", "")}</tns:last_transaction_description>
      </tns:GetAccountBalanceResult>
    </tns:GetAccountBalanceResponse>""")

    return soap_fault(f"Unknown operation: {local}"), 400


WSDL = f"""<?xml version="1.0" encoding="UTF-8"?>
<definitions name="AccountService"
  targetNamespace="{TNS}"
  xmlns="{TNS}"
  xmlns:soap="http://schemas.xmlsoap.org/wsdl/soap/"
  xmlns:wsdl="http://schemas.xmlsoap.org/wsdl/"
  xmlns:xsd="http://www.w3.org/2001/XMLSchema">

  <wsdl:message name="GetAccountBalanceRequest">
    <wsdl:part name="account_id" type="xsd:string"/>
  </wsdl:message>
  <wsdl:message name="GetAccountBalanceResponse">
    <wsdl:part name="account_id" type="xsd:string"/>
    <wsdl:part name="balance" type="xsd:string"/>
    <wsdl:part name="currency" type="xsd:string"/>
    <wsdl:part name="account_type" type="xsd:string"/>
    <wsdl:part name="status" type="xsd:string"/>
    <wsdl:part name="owner_name" type="xsd:string"/>
  </wsdl:message>

  <wsdl:portType name="AccountPortType">
    <wsdl:operation name="GetAccountBalance">
      <wsdl:input message="GetAccountBalanceRequest"/>
      <wsdl:output message="GetAccountBalanceResponse"/>
    </wsdl:operation>
  </wsdl:portType>

  <wsdl:binding name="AccountBinding" type="AccountPortType">
    <soap:binding style="rpc" transport="http://schemas.xmlsoap.org/soap/http"/>
    <wsdl:operation name="GetAccountBalance">
      <soap:operation soapAction="GetAccountBalance"/>
    </wsdl:operation>
  </wsdl:binding>

  <wsdl:service name="AccountService">
    <wsdl:port name="AccountPort" binding="AccountBinding">
      <soap:address location="http://localhost:8000/account"/>
    </wsdl:port>
  </wsdl:service>
</definitions>"""
