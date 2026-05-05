"""
SOAP Service: TransferService
Endpoint: /transfer
Operations: TransferFunds
"""
from datetime import datetime
from flask import Blueprint, request, Response
import xml.etree.ElementTree as ET
from data.mock_data import ACCOUNTS, transfer_counter

transfer_bp = Blueprint("transfer", __name__)

TNS = "http://paritybank.com/transfer"
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


@transfer_bp.route("", methods=["GET", "POST"])
def handle():
    if request.method == "GET":
        return Response(WSDL, mimetype="text/xml")

    root = ET.fromstring(request.data)
    body = root.find(f"{{{SOAP_NS}}}Body")
    op = next(iter(body), None) if body is not None else None
    if op is None:
        return soap_fault("Empty SOAP Body"), 400

    local = op.tag.split("}")[-1] if "}" in op.tag else op.tag

    if local == "TransferFunds":
        from_id = op.findtext(f"{{{TNS}}}from_account_id") or ""
        to_id = op.findtext(f"{{{TNS}}}to_account_id") or ""
        amount_str = op.findtext(f"{{{TNS}}}amount") or "0"
        reference = op.findtext(f"{{{TNS}}}reference") or ""

        from_acct = ACCOUNTS.get(from_id)
        to_acct = ACCOUNTS.get(to_id)

        if not from_acct:
            return soap_fault(f"Source account not found: {from_id}"), 404
        if not to_acct:
            return soap_fault(f"Destination account not found: {to_id}"), 404
        if from_acct["status"] == "FROZEN":
            return soap_fault(f"Source account is frozen: {from_id}"), 400

        amount = float(amount_str)
        from_bal = float(from_acct["balance"])
        to_bal = float(to_acct["balance"])

        if from_bal < amount:
            return soap_fault("Insufficient funds"), 400

        from_after = from_bal - amount
        to_after = to_bal + amount
        ACCOUNTS[from_id]["balance"] = f"{from_after:.2f}"
        ACCOUNTS[to_id]["balance"] = f"{to_after:.2f}"

        transfer_counter[0] += 1
        conf_id = f"TRF-{transfer_counter[0]:06d}"
        ts = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S")

        return soap_envelope(f"""
    <tns:TransferFundsResponse>
      <tns:TransferFundsResult>
        <tns:confirmation_id>{conf_id}</tns:confirmation_id>
        <tns:status>COMPLETED</tns:status>
        <tns:timestamp>{ts}</tns:timestamp>
        <tns:from_account_id>{from_id}</tns:from_account_id>
        <tns:to_account_id>{to_id}</tns:to_account_id>
        <tns:amount>{amount:.2f}</tns:amount>
        <tns:from_balance_after>{from_after:.2f}</tns:from_balance_after>
        <tns:to_balance_after>{to_after:.2f}</tns:to_balance_after>
        <tns:message>Transfer completed. Reference: {reference}</tns:message>
      </tns:TransferFundsResult>
    </tns:TransferFundsResponse>""")

    return soap_fault(f"Unknown operation: {local}"), 400


WSDL = f"""<?xml version="1.0" encoding="UTF-8"?>
<definitions name="TransferService"
  targetNamespace="{TNS}"
  xmlns="{TNS}"
  xmlns:soap="http://schemas.xmlsoap.org/wsdl/soap/"
  xmlns:wsdl="http://schemas.xmlsoap.org/wsdl/"
  xmlns:xsd="http://www.w3.org/2001/XMLSchema">

  <wsdl:service name="TransferService">
    <wsdl:port name="TransferPort" binding="TransferBinding">
      <soap:address location="http://localhost:8000/transfer"/>
    </wsdl:port>
  </wsdl:service>
</definitions>"""
