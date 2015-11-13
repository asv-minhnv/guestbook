define([
		"doh"
		"guestbook.model.Greeting"
	],function(doh, Greeting){
		doh.register(guestbook.model.Greeting,[
			name: 'setter',
			runTest: function(){
			var greeting = new Greeting();
			greeting.set({

			})
		}
		])
	}

)