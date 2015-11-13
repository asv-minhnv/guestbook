define([
	"doh/runner",
	"guestbook/view/GuestbookView",
	"guestbook/GuestbookStore"
], function(doh, GuestbookView, GuestbookStore) {

	doh.register("MyTests", [
		function assertTrueTest() {
			doh.assertTrue(true);
			doh.assertTrue(1);
			doh.assertTrue(!false);
		},
		{
			name: "guestbook",
			setUp: function () {
				var guestbookName = "default_guestbook";
				var store = new GuestbookStore({"guestbookName": guestbookName});
				this.guestbook = new GuestbookView({
					"guestbookName": guestbookName,
					"guestbookStore": store
				});
			},
			runTest: function () {
				var guestBook = this.guestbook.addNewGreeting();
				console.log(guestBook);
				//doh.assertEqual("blah", this.thingerToTest.blahProp);
				//doh.assertFalse(this.thingerToTest.falseProp);
				//
			},
			tearDown: function () {
			}

		}
	]);

});
