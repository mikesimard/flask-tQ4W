from flask import Flask, request, make_response
from http.cookies import SimpleCookie
from urllib.parse import parse_qs
import http.cookies

app = Flask(__name__)

@app.route('/referrer')
def home():
    response_html =  "<h1>Test Link</h1><ul>"
    response_html += "<li><a href='⁠https://landing.brazzersnetwork.com/?ad_id=176_rev&ats=eyJhIjoxNzYsImMiOjMxMzMzLCJuIjoxNCwicyI6OTAsImUiOjg4MDMsInAiOjJ9&apb=2614%7C%7COTYuMjEuMTUyLjEwOQ%3D%3D'>Link with params (ATS,ACLID)</a></li>"
    response_html += "<li><a href='⁠https://landing.brazzersnetwork.com/?ad_id=176_rev&ats=eyJhIjoxNzYsImMiOjMxMzMzLCJuIjoxNCwicyI6OTAsImUiOjg4MDMsInAiOjJ9&apb=2614%7C%7COTYuMjEuMTUyLjEwOQ%3D%3D&lang=en&page_id=20983'>Link with params (ATS,ACLID,LANG,PAGE_ID)</a></li>"
    response_html += "</ul></body>"
    return response_html

@app.route('/about')
def about():
    return 'This is the about page.'

@app.route('/landing')
def show_info():
    # Get all HTTP headers
    headers = dict(request.headers)

    # Get the query parameters from request.args
    query_params = request.args.to_dict()

    # Create a response
    response = make_response("Query parameters captured and stored as cookies.")

    # Set each query parameter as a cookie
    for param, value in query_params.items():
        response.set_cookie(param, value)



    # Get all cookies
    cookies = request.cookies

    # Get all query parameters
    query_params = request.args


    response_html = """ <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Header, Cookies, and Window Location Details</title>
        <script src="https://www.nutaku.net/js/atlaslib.min.js?20220511170233"></script>
        <script src="https://www.nutaku.net/js/vortex.modern.min.js?20230908152747"></script>
        <script>
            atlas.init({
                affUrl: "nutaku.net",
                networkCode: "NTK",
                defaultCode: "eyJhIjozLCJjIjozLCJuIjoxLCJzIjoxLCJlIjoyLCJwIjozfQ",
                //usePrimaryDomainForEtahub: true,
                useSecureCookies: false,
                debug: true
            });
    
            atlas.autoTrack();
    
            console.log(atlas.storage());
            console.log(atlas.getDecodedReferralCode());

        </script>
       
    </head>
    <body>
      <h1>Back-end Output</h1>
    """

    # Create an HTML response to display the information
    response_html += "<h2>HTTP Headers:</h2>"
    response_html += "<pre><code>" + json_format(headers) + "</code></pre>"

    response_html += "<h2>Cookies:</h2>"
    response_html += "<pre><code>" + json_format(cookies) + "</code></pre>"

    response_html += "<h2>Query Parameters:</h2>"
    response_html += "<pre><code>" + json_format(query_params) + "</code></pre>"

    response_html += """ <h1>Browser Output</h1>
    <pre id="output"></pre>

<script>
    // Function to format and display the data
    function displayData() {
        const headers = JSON.stringify(getHeaders(), null, 2);
        const cookies = JSON.stringify(getCookies(), null, 2);
        const location = window.location.href;
        const output = `Headers:\n${headers}\n\nCookies:\n${cookies}\n\nWindow Location:\n${location}`;
        document.getElementById('output').textContent = output;
    }

    // Function to get headers
    function getHeaders() {
        const xhr = new XMLHttpRequest();
        xhr.open('HEAD', window.location.href, false);
        xhr.send(null);
        
        const headersObject = {};
        const headersArray = xhr.getAllResponseHeaders().trim().split('\\n');
        headersArray.forEach(header => {
            const [name, value] = header.split(': ');
            headersObject[name] = value;
        });
        
        return headersObject;
    }

    // Function to get cookies
    function getCookies() {
        const cookiesObject = {};
        if (typeof document.cookie !== 'undefined') {
            document.cookie.split('; ').forEach(cookie => {
                const [name, value] = cookie.split('=');
                cookiesObject[name] = value;
            });
        } else {
            cookiesObject['Not Supported'] = 'Cookies API not available in this browser';
        }
        return cookiesObject;
    }

    // Call the function to display the data
    displayData();
</script>
    </body>
    </html>
    """

    response.set_data(response_html)
    return response


@app.after_request
def after(response):
    # todo with response
    print(response.status)
    print(response.headers)

    return response


def json_format(data):
    import json
    return json.dumps(data, indent=4)



if __name__ == '__main__':
    app.run()
