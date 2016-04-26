import aiohttp
import asyncio
import ssl
import sys
import re
def get():
    print("Starting")
    try:
        conn = aiohttp.TCPConnector(verify_ssl=True,)
        session = aiohttp.ClientSession(connector=conn)
        r = yield from session.request("get",'https://superfish.badssl.com/',allow_redirects=False)
        if r.status==301:
            print(r.headers["Location"])
        print(r.headers)
        content = yield from r.text()

        session.close()
        return content
    except ssl.CertificateError as e:
        errorString=str(e)
        if "[[SSL: CERTIFICATE_VERIFY_FAILED]"in errorString:
            print("bad ssl cert")
        session.close()
        print(errorString)
    except ssl.CertificateError as e:
        print(str(e))


loop = asyncio.get_event_loop()
s=loop.run_until_complete(get())
print(s)
