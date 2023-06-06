from django.conf import settings
from django.http import JsonResponse, HttpResponse
from random import randint
from . import mailing
import requests
import hashlib
import base64
import json
import random


def random_of_digits(n):
    range_start = 10 ** (n - 1)
    range_end = (10 ** n) - 1
    return randint(range_start, range_end)


# Use the system PRNG if po ssible
try:
    random = random.SystemRandom()
    using_sysrandom = True
except NotImplementedError:
    import warnings

    warnings.warn('A secure pseudo-random number generator is not available '
                  'on your system. Falling back to Mersenne Twister.')
    using_sysrandom = False


def send_mail(user_mail, subject, message):
    email_content = """
    <!DOCTYPE><html><head><title>Epsumthings</title><meta http-equiv="Content-Type" content="text/html; charset=utf-8"/><meta name="viewport" content="width=device-width, initial-scale=1.0"/><style type="text/css">a{outline:none;color:#40aceb;text-decoration:underline;}a:hover{text-decoration:none !important;}.nav a:hover{text-decoration:underline !important;}.title a:hover{text-decoration:underline !important;}.title-2 a:hover{text-decoration:underline !important;}.btn:hover{opacity:0.8;}.btn a:hover{text-decoration:none !important;}.btn{-webkit-transition:all 0.3s ease;-moz-transition:all 0.3s ease;-ms-transition:all 0.3s ease;transition:all 0.3s ease;}table td{border-collapse: collapse !important;}.ExternalClass, .ExternalClass a, .ExternalClass span, .ExternalClass b, .ExternalClass br, .ExternalClass p, .ExternalClass div{line-height:inherit;}@media only screen and (max-width:500px){table[class="flexible"]{width:100% !important;}table[class="center"]{float:none !important;margin:0 auto !important;}*[class="hide"]{display:none !important;width:0 !important;height:0 !important;padding:0 !important;font-size:0 !important;line-height:0 !important;}td[class="img-flex"] img{width:100% !important;height:auto !important;}td[class="aligncenter"]{text-align:center !important;}th[class="flex"]{display:block !important;width:100% !important;}td[class="wrapper"]{padding:0 !important;}td[class="holder"]{padding:30px 15px 20px !important;}td[class="nav"]{padding:20px 0 0 !important;text-align:center !important;}td[class="h-auto"]{height:auto !important;}td[class="description"]{padding:30px 20px !important;}td[class="i-120"] img{width:120px !important;height:auto !important;}td[class="footer"]{padding:5px 20px 20px !important;}td[class="footer"] td[class="aligncenter"]{line-height:25px !important;padding:20px 0 0 !important;}tr[class="table-holder"]{display:table !important;width:100% !important;}th[class="thead"]{display:table-header-group !important; width:100% !important;}th[class="tfoot"]{display:table-footer-group !important; width:100% !important;}}</style></head><body style="margin:0; padding:0;" bgcolor="#eaeced"><table style="min-width:320px;" width="100%" cellspacing="0" cellpadding="0" bgcolor="#eaeced"><tr><td class="hide"><table width="600" cellpadding="0" cellspacing="0" style="width:600px !important;"><tr><td style="min-width:600px; font-size:0; line-height:0;">&nbsp;</td></tr></table></td></tr><tr><td class="wrapper" style="padding:0 10px;"><table data-module="module-1" data-thumb="thumbnails/01.png" width="100%" cellpadding="0" cellspacing="0"><tr><td data-bgcolor="bg-module" bgcolor="#eaeced"><table class="flexible" width="600" align="center" style="margin:0 auto;" cellpadding="0" cellspacing="0"><tr><td style="padding:29px 0 30px;"><table width="100%" cellpadding="0" cellspacing="0"><tr><th class="flex" width="113" align="left" style="padding:0;"><table class="center" cellpadding="0" cellspacing="0"><tr><td style="line-height:0;"><a target="_blank" style="text-decoration:none;" href="https://www.epsumlabs.com"><img src="https://epsumlabs.com/assets/img/logo/epsm.png" border="0" style="font:bold 12px/12px Arial, Helvetica, sans-serif; color:#606060;" align="left" vspace="0" hspace="0" width="60%" alt="EPSUMLABS.COM"/></a></td></tr></table></th><th class="flex" align="left" style="padding:0;"><table width="100%" cellpadding="0" cellspacing="0"><tr><td data-color="text" data-size="size navigation" data-min="10" data-max="22" data-link-style="text-decoration:none; color:#888;" class="nav" align="right" style="font:bold 13px/15px Arial, Helvetica, sans-serif; color:#888;"><a target="_blank" style="text-decoration:none; color:#888;" href="https://epsumlabs.com">Home</a>&nbsp; &nbsp; <a target="_blank" style="text-decoration:none; color:#888;" href="https://epsumlabs.com/contact.html">Contact</a></td></tr></table></th></tr></table></td></tr></table></td></tr></table><table data-module="module-2" data-thumb="thumbnails/02.png" width="100%" cellpadding="0" cellspacing="0"><tr><td data-bgcolor="bg-module" bgcolor="#eaeced"><table class="flexible" width="600" align="center" style="margin:0 auto;" cellpadding="0" cellspacing="0"><tr><td data-bgcolor="bg-block" class="holder" style="padding:58px 60px 52px;" bgcolor="#f9f9f9"><table width="100%" cellpadding="0" cellspacing="0"><tr><td data-color="title" data-size="size title" data-min="25" data-max="45" data-link-color="link title color" data-link-style="text-decoration:none; color:#292c34;" class="title" align="center" style="font:35px/38px Arial, Helvetica, sans-serif; color:#292c34; padding:0 0 24px;">""" + subject + """</td></tr><tr><td data-color="text" data-size="size text" data-min="10" data-max="26" data-link-color="link text color" data-link-style="font-weight:bold; text-decoration:underline; color:#40aceb;" align="center" style="font:bold 16px/25px Arial, Helvetica, sans-serif; color:#888; padding:0 0 23px;">""" \
                    + message \
                    + """</td></tr></table></td></tr><tr><td height="28"></td></tr></table></td></tr></table><table data-module="module-7" data-thumb="thumbnails/07.png" width="100%" cellpadding="0" cellspacing="0"><tr><td data-bgcolor="bg-module" bgcolor="#eaeced"><table class="flexible" width="600" align="center" style="margin:0 auto;" cellpadding="0" cellspacing="0"><tr><td class="footer" style="padding:0 0 10px;"><table width="100%" cellpadding="0" cellspacing="0"><tr class="table-holder"><th class="tfoot" width="400" align="left" style="vertical-align:top; padding:0;"><table width="100%" cellpadding="0" cellspacing="0"><tr><td data-color="text" data-link-color="link text color" data-link-style="text-decoration:underline; color:#797c82;" class="aligncenter" style="font:12px/16px Arial, Helvetica, sans-serif; color:#797c82; padding:0 0 10px;">Epsum Labs Private Limited, 2017. &nbsp; All Rights Reserved. <a target="_blank" style="text-decoration:underline; color:#797c82;">Please Do Not Reply.</a></td></tr></table></th></tr></table></td></tr></table></td></tr></table></td></tr><tr><td style="line-height:0;"><div style="display:none; white-space:nowrap; font:15px/1px courier;">&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;</div></td></tr></table></body></html>"""
    mailing.send_mail(subject, email_content, user_mail, "support@epsumlabs.com")


def send_notification(tokens, message, title):
    url = 'https://fcm.googleapis.com/fcm/send'
    fields = {'registration_ids': tokens,
              'notification': {
                  'title': title,
                  'body': message,
                  'sound': 'sound.mp3'
              }}
    headers = {
        'Authorization': 'key = AAAAw8rUA9I:APA91bFK-t01jFCArF517EFA6kVm4onDQwZx9tQBfRGBkhNOSr08j3FQDXxU5hm-U2loMZClUYjPpZeo229LiH52ZpNubpnLD3iWsJUkEcDAcsCUWFa-U6_g4StdCZTHBxdYlmgOEG3V',
        'Content-Type': 'application/json'}
    response = requests.post(url=url, headers=headers, data=json.dumps(fields))

    response_ = response.text
    print(response_)
    return response_


def base64ofsha(input):
    s = hashlib.sha256(input.encode('utf-8')).digest()
    return str(base64.b64encode(s), encoding="utf-8")


def base64decode(string):
    return str(base64.b64decode(string), "utf-8")


def json_response(response, status=200):
    res = JsonResponse(response, status=status)
    res["Access-Control-Allow-Origin"] = "*"
    res["Content-Type"] = "application/json; charset=utf-8"
    return res


def json_success_response(data, status=200):
    res = JsonResponse({"status": 'success', "data": data}, status=status)
    res["Access-Control-Allow-Origin"] = "*"
    res["Content-Type"] = "application/json; charset=utf-8"
    return res


def json_error_response(message):
    res = JsonResponse({"status": "failed", "msg": message}, status=401)
    res["Access-Control-Allow-Origin"] = "*"
    res["Content-Type"] = "application/json; charset=utf-8"
    return res


# not used
def error(err):
    try:

        res = JsonResponse({"status": "failed", "message": str(err.message)})
        res["Access-Control-Allow-Origin"] = "*"
        res["Content-Type"] = "application/json; charset=utf-8"
        return res
    except Exception:
        res = JsonResponse({"status": "failed", 'message': str(err)})
        res["Access-Control-Allow-Origin"] = "*"
        res["Content-Type"] = "application/json; charset=utf-8"
        return res


def preflight(request):
    res = HttpResponse('', "application/json", status=200)
    res["Access-Control-Allow-Origin"] = request.META["HTTP_ORIGIN"]
    res["Access-Control-Allow-Headers"] = "*"
    res["Access-Control-Expose-Headers"] = "authorization,user"
    res["Access-Control-Allow-Credentials"] = "true"
    res["Access-Control-Allow-Methods"] = "POST, PUT, GET, OPTIONS, DELETE"
    return res


failure_dict = {"status": "failed"}
