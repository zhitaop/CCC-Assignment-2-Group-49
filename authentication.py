class authentication:

    def __init__(self):
        # Go to http://apps.twitter.com and create an app.
		# The consumer key and secret will be generated for you after
        self.consumer_key ="ovzZpAxizMf40aRBebETy65vR"
        self.consumer_secret="4UR8d3JoAN6SNYblgq8XtV0xdsutv4MPawAqI9Ob7yyahfX65l"

		# After the step above, you will be redirected to your app's page.
		# Create an access token under the the "Your access token" section
        self.access_token="967777720150052865-X2fTRFP6uauYsqrvE12aDewhuIXNNEf"
        self.access_token_secret="z1O9hIYt8QKps2I73ZjrFAvWIq8m9ZsVkAUStUVw2kSXX"

    def getconsumer_key(self):
        return self.consumer_key
    def getconsumer_secret(self):
        return self.consumer_secret
    def getaccess_token(self):
        return self.access_token
    def getaccess_token_secret(self):
        return self.access_token_secret