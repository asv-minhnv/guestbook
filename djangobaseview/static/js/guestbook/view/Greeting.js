define([
	"dojo/_base/declare",
	"dojo/_base/lang",
	"dojo/on",
	"dojo/dom-style",
	"dojo/text!./templates/Greeting.html",
	"./_ViewBaseMixin"

], function(declare, lang, on, domStyle, template, _ViewBaseMixin){

		return declare("WidgetGreeting", [_ViewBaseMixin], {

			templateString: template,
			guestbookStore: null,
			guestbookName: "",
			greeting_id: "",
			author: "",
			content: "",
			date: "",

			constructor: function(data){
				this.guestbookName = data.guestbook_name;
				this.greeting_id = data.greeting_id;
				this.content = data.content;
				this.date = data.date;
				if (data.updated_by !== "None"){
					this.author = data.updated_by;
				}else{
					this.author = "Anonymous Person";
				}
				this.guestbookStore = data.guestbook_store;
			},

			postCreate: function(data){
				this.inherited(arguments);

				this.own(
					on(this.deleteButton,
						"click", lang.hitch(this, "deleteGreeting")),
					on(this.openEditFormButton,
						"click", lang.hitch(this, "openEditForm")),
					on(this.submitUpdateGreetingButton,
						"click", lang.hitch(this, "updateGreeting"))
				);
			},

			deleteGreeting: function(){
				this.guestbookStore.set("guestbookName", this.guestbookName);
				this.guestbookStore.deleteGreeting(this.greeting_id)
					.then(lang.hitch(this, function(data){
						alert("Delete Success");
						this.destroyRecursive();
				}), function(error){
					alert(error);
				});
			},

			openEditForm: function(){
				this.guestbookStore.set("guestbookName", this.guestbookName);
				this.guestbookStore.getGreetingDetail(this.greeting_id)
					.then(lang.hitch(this, function(data){
						var formNode = this.editFormNode;
						domStyle.set(formNode, {"display": "block"});
						this.textEditGreeting.set("value", data.content);
				}), function(error){
					alert(error);
				});
			},

			updateGreeting: function(){
				if (this.textEditGreeting.validate() == true) {
					this.content = this.textEditGreeting.value
					this.guestbookStore.set("guestbookName", this.guestbookName);
					this.guestbookStore.updateGreeting(this.greeting_id, this.content)
						.then(lang.hitch(this, function () {
							alert("Update Success");
							this.contentNode.innerHTML = this.content
							var formNode = this.editFormNode;
							domStyle.set(formNode, {"display": "none"});
						}), function (error) {
							alert(error);
						})
				}else{
					alert("Form Invalid");
				}
			}
		});
});