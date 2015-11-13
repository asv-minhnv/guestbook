define([
	"doh/runner",
	"guestbook/view/GreetingView"
], function(doh, GreetingView){
	doh.register("GreetingTest", [
		function assertTrueTest(){
		doh.assertTrue(true);
		doh.assertTrue(1);
		doh.assertTrue(!false);
	  },
	  {
		name: "greeting",
		setUp: function(){
			this.abc = 1;

			//this.greeting = new GreetingView();
			//var guestbookName = "default_guestbook";
			//var store = new GuestbookStore({"guestbookName": guestbookName});
			//var guestbook = new GuestbookView({
			//	"guestbookName": guestbookName,
			//	"guestbookStore": store
			//});
			//this.thingerToTest.doStuffToInit();
		},
		runTest: function(){
			console.log(this.abc);
			doh.assertEqual(3, this.abc);
			doh.assertFalse(this.abc);
		  //doh.assertEqual("blah", this.thingerToTest.blahProp

			//var add = this.greeting.delete('')
		  //
		},
		tearDown: function(){
		}
	  },
	  //
	]);

});
