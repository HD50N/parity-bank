"""
SOAP Service: TransactionService
Endpoint: /transaction
Operations: GetTransactionHistory
"""
from flask import Blueprint, request, Response
import xml.etree.ElementTree as ET
from data.mock_data import TRANSACTIONS

transaction_bp = Blueprint("transaction", __name__)

TNS = "http://paritybank.com/transaction"
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


@transaction_bp.route("", methods=["GET", "POST"])
def handle():
    if request.method == "GET":
        return Response(WSDL, mimetype="text/xml")

    root = ET.fromstring(request.data)
    body = root.find(f"{{{SOAP_NS}}}Body")
    op = next(iter(body), None) if body is not None else None
    if op is None:
        return soap_fault("Empty SOAP Body"), 400

    local = op.tag.split("}")[-1] if "}" in op.tag else op.tag

    if local == "GetTransactionHistory":
        account_id = op.findtext(f"{{{TNS}}}account_id") or ""
        from_date = op.findtext(f"{{{TNS}}}from_date") or ""
        to_date = op.findtext(f"{{{TNS}}}to_date") or ""

        txns = TRANSACTIONS.get(account_id, [])
        if from_date or to_date:
            filtered = []
            for t in txns:
                d = t["date"][:10]
                if from_date and d < from_date[:10]:
                    continue
                if to_date and d > to_date[:10]:
                    continue
                filtered.append(t)
            txns = filtered

        items_xml = ""
        for t in txns:
            items_xml += f"""
          <tns:TransactionItem>
            <tns:id>{t["id"]}</tns:id>
            <tns:amount>{t["amount"]}</tns:amount>
            <tns:date>{t["date"]}</tns:date>
            <tns:description>{t["description"]}</tns:description>
            <tns:type>{t["type"]}</tns:type>
            <tns:balance_after>{t["balance_after"]}</tns:balance_after>
          </tns:TransactionItem>"""

        return soap_envelope(f"""
    <tns:GetTransactionHistoryResponse>
      <tns:GetTransactionHistoryResult>
        <tns:account_id>{account_id}</tns:account_id>
        <tns:from_date>{from_date}</tns:from_date>
        <tns:to_date>{to_date}</tns:to_date>
        <tns:transaction_count>{len(txns)}</tns:transaction_count>
        <tns:transactions>{items_xml}
        </tns:transactions>
      </tns:GetTransactionHistoryResult>
    </tns:GetTransactionHistoryResponse>""")

    return soap_fault(f"Unknown operation: {local}"), 400


WSDL = f"""<?xml version="1.0" encoding="UTF-8"?>
<definitions name="TransactionService"
  targetNamespace="{TNS}"
  xmlns="{TNS}"
  xmlns:soap="http://schemas.xmlsoap.org/wsdl/soap/"
  xmlns:wsdl="http://schemas.xmlsoap.org/wsdl/"
  xmlns:xsd="http://www.w3.org/2001/XMLSchema">

  <wsdl:portType name="TransactionPortType">
    <wsdl:operation name="GetTransactionHistory">
      <wsdl:input message="GetTransactionHistoryRequest"/>
      <wsdl:output message="GetTransactionHistoryResponse"/>
    </wsdl:operation>
  </wsdl:portType>

  <wsdl:service name="TransactionService">
    <wsdl:port name="TransactionPort" binding="TransactionBinding">
      <soap:address location="http://localhost:8000/transaction"/>
    </wsdl:port>
  </wsdl:service>
</definitions>"""
