"""
SOAP Service: CustomerService
Endpoint: /customer
Operations: GetCustomerInfo
"""
from flask import Blueprint, request, Response
import xml.etree.ElementTree as ET
from data.mock_data import CUSTOMERS

customer_bp = Blueprint("customer", __name__)

TNS = "http://paritybank.com/customer"
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


@customer_bp.route("", methods=["GET", "POST"])
def handle():
    if request.method == "GET":
        return Response(WSDL, mimetype="text/xml")

    root = ET.fromstring(request.data)
    body = root.find(f"{{{SOAP_NS}}}Body")
    op = next(iter(body), None) if body is not None else None
    if op is None:
        return soap_fault("Empty SOAP Body"), 400

    local = op.tag.split("}")[-1] if "}" in op.tag else op.tag

    if local == "GetCustomerInfo":
        customer_id = op.findtext(f"{{{TNS}}}customer_id") or ""
        customer = CUSTOMERS.get(customer_id)
        if not customer:
            return soap_fault(f"Customer not found: {customer_id}"), 404

        return soap_envelope(f"""
    <tns:GetCustomerInfoResponse>
      <tns:GetCustomerInfoResult>
        <tns:customer_id>{customer["customer_id"]}</tns:customer_id>
        <tns:first_name>{customer["first_name"]}</tns:first_name>
        <tns:last_name>{customer["last_name"]}</tns:last_name>
        <tns:email>{customer["email"]}</tns:email>
        <tns:phone>{customer["phone"]}</tns:phone>
        <tns:address>{customer["address"]}</tns:address>
        <tns:primary_account_id>{customer["primary_account_id"]}</tns:primary_account_id>
      </tns:GetCustomerInfoResult>
    </tns:GetCustomerInfoResponse>""")

    return soap_fault(f"Unknown operation: {local}"), 400


WSDL = f"""<?xml version="1.0" encoding="UTF-8"?>
<definitions name="CustomerService"
  targetNamespace="{TNS}"
  xmlns="{TNS}"
  xmlns:soap="http://schemas.xmlsoap.org/wsdl/soap/"
  xmlns:wsdl="http://schemas.xmlsoap.org/wsdl/"
  xmlns:xsd="http://www.w3.org/2001/XMLSchema">

  <wsdl:service name="CustomerService">
    <wsdl:port name="CustomerPort" binding="CustomerBinding">
      <soap:address location="http://localhost:8000/customer"/>
    </wsdl:port>
  </wsdl:service>
</definitions>"""
