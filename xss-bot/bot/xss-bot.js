var page = require('webpage').create();
var host = "web";
var url = "http://"+host+":5000/login_attempts";
var timeout = 2000;

phantom.addCookie({
      'name': 'flag',
      'value': 'leoctf{xss_c4n_b3_d4ng3r0u5}',
      'domain': host,
      'path': '/',
      'httponly': false
});

phantom.addCookie({
      'name': 'session',
      'value': '.eJyrVkpMyc3MU7Iy1FHKTAFTOfnp6akp8SDBkqLSVB2l0uLUorzE3FQlK6jiWgDXuRHC.YYHGXw._WPyii_vsWLw8Q3xObmKzOGViAk',
      'domain': host,
      'path': '/',
      'httponly': false
});

page.settings.resourceTimeout = timeout;

page.open(url, function(status) {
      setTimeout(function(){
                phantom.exit();
            }, 1);
});
