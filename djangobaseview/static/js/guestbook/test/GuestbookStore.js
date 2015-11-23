define([
	"doh/runner",
	'dojo/json',
	'dojo/topic',
	'dojo/_base/array',
	"dojo/_base/declare",
	"dojo/store/JsonRest",
	"dojo/cookie",
	"dojo/Stateful",
	"./sinon",
	"guestbook/view/GuestbookView",
	"guestbook/GuestbookStore"
], function(doh, json, topic, array, declare, JsonRest, cookie, Stateful, sinon, GuestbookView, GuestbookStore) {

	doh.register('guestbook.test.GuestbookStore', {

		testGetGreeting: sinon.test(function () {

			var deferred = new doh.Deferred(),
				guestbookName = "default_guestbook";
			guestbookstore = new GuestbookStore({"guestbookName": guestbookName});
			results = [
				{"is_admin": false, "content": "guestbook message b", "date": "2015-11-13 03:32:12.534089", "user_info": "None", "greeting_id": 5225978766819328, "updated_by": "", "updated_date": "2015-11-13 03:32:12.534094", "guestbook_name": "default_guestbook"}, {"is_admin": false, "content": "guestbook message b", "date": "2015-11-13 03:32:12.395630", "user_info": "None", "greeting_id": 5788928720240640, "updated_by": "", "updated_date": "2015-11-13 03:32:12.395641", "guestbook_name": "default_guestbook"}, {"is_admin": false, "content": "guestbook message b", "date": "2015-11-13 03:32:02.844759", "user_info": "None", "greeting_id": 4663028813398016, "updated_by": "", "updated_date": "2015-11-13 03:32:02.844763", "guestbook_name": "default_guestbook"}, {"is_admin": false, "content": "guestbook message b", "date": "2015-11-13 03:32:02.843229", "user_info": "None", "greeting_id": 6492616162017280, "updated_by": "", "updated_date": "2015-11-13 03:32:02.843235", "guestbook_name": "default_guestbook"}, {"is_admin": false, "content": "guestbook message b", "date": "2015-11-13 03:31:46.010807", "user_info": "None", "greeting_id": 5366716255174656, "updated_by": "", "updated_date": "2015-11-13 03:31:46.010810", "guestbook_name": "default_guestbook"}, {"is_admin": false, "content": "guestbook message b", "date": "2015-11-13 03:31:46.009354", "user_info": "None", "greeting_id": 5929666208595968, "updated_by": "", "updated_date": "2015-11-13 03:31:46.009360", "guestbook_name": "default_guestbook"}, {"is_admin": false, "content": "guestbook message b", "date": "2015-11-13 03:31:27.005385", "user_info": "None", "greeting_id": 4803766301753344, "updated_by": "", "updated_date": "2015-11-13 03:31:27.005388", "guestbook_name": "default_guestbook"}, {"is_admin": false, "content": "guestbook message b", "date": "2015-11-13 03:31:27.003940", "user_info": "None", "greeting_id": 6211141185306624, "updated_by": "", "updated_date": "2015-11-13 03:31:27.003945", "guestbook_name": "default_guestbook"}, {"is_admin": false, "content": "guestbook message b", "date": "2015-11-13 03:31:00.478493", "user_info": "None", "greeting_id": 5085241278464000, "updated_by": "", "updated_date": "2015-11-13 03:31:00.478499", "guestbook_name": "default_guestbook"}, {"is_admin": false, "content": "guestbook message b", "date": "2015-11-13 03:31:00.444216", "user_info": "None", "greeting_id": 5648191231885312, "updated_by": "", "updated_date": "2015-11-13 03:31:00.444223", "guestbook_name": "default_guestbook"}, {"is_admin": false, "content": "guestbook message b", "date": "2015-11-13 03:29:26.808801", "user_info": "None", "greeting_id": 4522291325042688, "updated_by": "", "updated_date": "2015-11-13 03:29:26.808804", "guestbook_name": "default_guestbook"}, {"is_admin": false, "content": "guestbook message b", "date": "2015-11-13 03:29:26.807145", "user_info": "None", "greeting_id": 6721314580594688, "updated_by": "", "updated_date": "2015-11-13 03:29:26.807150", "guestbook_name": "default_guestbook"}, {"is_admin": false, "content": "guestbook message b", "date": "2015-11-13 03:29:03.829938", "user_info": "None", "greeting_id": 5595414673752064, "updated_by": "", "updated_date": "2015-11-13 03:29:03.829941", "guestbook_name": "default_guestbook"}, {"is_admin": false, "content": "guestbook message b", "date": "2015-11-13 03:29:03.828506", "user_info": "None", "greeting_id": 6158364627173376, "updated_by": "", "updated_date": "2015-11-13 03:29:03.828510", "guestbook_name": "default_guestbook"}, {"is_admin": false, "content": "guestbook message b", "date": "2015-11-13 03:27:31.930525", "user_info": "None", "greeting_id": 5032464720330752, "updated_by": "", "updated_date": "2015-11-13 03:27:31.930545", "guestbook_name": "default_guestbook"}, {"is_admin": false, "content": "guestbook message b", "date": "2015-11-13 03:27:31.780663", "user_info": "None", "greeting_id": 6439839603884032, "updated_by": "", "updated_date": "2015-11-13 03:27:31.780669", "guestbook_name": "default_guestbook"}, {"is_admin": false, "content": "guestbook message b", "date": "2015-11-13 03:27:10.486645", "user_info": "None", "greeting_id": 5313939697041408, "updated_by": "", "updated_date": "2015-11-13 03:27:10.486651", "guestbook_name": "default_guestbook"}, {"is_admin": false, "content": "guestbook message b", "date": "2015-11-13 03:27:10.304004", "user_info": "None", "greeting_id": 5876889650462720, "updated_by": "", "updated_date": "2015-11-13 03:27:10.304020", "guestbook_name": "default_guestbook"}, {"is_admin": false, "content": "guestbook message b", "date": "2015-11-13 03:25:41.710036", "user_info": "None", "greeting_id": 4750989743620096, "updated_by": "", "updated_date": "2015-11-13 03:25:41.710040", "guestbook_name": "default_guestbook"}, {"is_admin": false, "content": "guestbook message b", "date": "2015-11-13 03:25:41.708163", "user_info": "None", "greeting_id": 6580577092239360, "updated_by": "", "updated_date": "2015-11-13 03:25:41.708169", "guestbook_name": "default_guestbook"}
			],
			expected = [
				{"is_admin": false, "content": "guestbook message b", "date": "2015-11-13 03:32:12.534089", "user_info": "None", "greeting_id": 5225978766819328, "updated_by": "", "updated_date": "2015-11-13 03:32:12.534094", "guestbook_name": "default_guestbook"}, {"is_admin": false, "content": "guestbook message b", "date": "2015-11-13 03:32:12.395630", "user_info": "None", "greeting_id": 5788928720240640, "updated_by": "", "updated_date": "2015-11-13 03:32:12.395641", "guestbook_name": "default_guestbook"}, {"is_admin": false, "content": "guestbook message b", "date": "2015-11-13 03:32:02.844759", "user_info": "None", "greeting_id": 4663028813398016, "updated_by": "", "updated_date": "2015-11-13 03:32:02.844763", "guestbook_name": "default_guestbook"}, {"is_admin": false, "content": "guestbook message b", "date": "2015-11-13 03:32:02.843229", "user_info": "None", "greeting_id": 6492616162017280, "updated_by": "", "updated_date": "2015-11-13 03:32:02.843235", "guestbook_name": "default_guestbook"}, {"is_admin": false, "content": "guestbook message b", "date": "2015-11-13 03:31:46.010807", "user_info": "None", "greeting_id": 5366716255174656, "updated_by": "", "updated_date": "2015-11-13 03:31:46.010810", "guestbook_name": "default_guestbook"}, {"is_admin": false, "content": "guestbook message b", "date": "2015-11-13 03:31:46.009354", "user_info": "None", "greeting_id": 5929666208595968, "updated_by": "", "updated_date": "2015-11-13 03:31:46.009360", "guestbook_name": "default_guestbook"}, {"is_admin": false, "content": "guestbook message b", "date": "2015-11-13 03:31:27.005385", "user_info": "None", "greeting_id": 4803766301753344, "updated_by": "", "updated_date": "2015-11-13 03:31:27.005388", "guestbook_name": "default_guestbook"}, {"is_admin": false, "content": "guestbook message b", "date": "2015-11-13 03:31:27.003940", "user_info": "None", "greeting_id": 6211141185306624, "updated_by": "", "updated_date": "2015-11-13 03:31:27.003945", "guestbook_name": "default_guestbook"}, {"is_admin": false, "content": "guestbook message b", "date": "2015-11-13 03:31:00.478493", "user_info": "None", "greeting_id": 5085241278464000, "updated_by": "", "updated_date": "2015-11-13 03:31:00.478499", "guestbook_name": "default_guestbook"}, {"is_admin": false, "content": "guestbook message b", "date": "2015-11-13 03:31:00.444216", "user_info": "None", "greeting_id": 5648191231885312, "updated_by": "", "updated_date": "2015-11-13 03:31:00.444223", "guestbook_name": "default_guestbook"}, {"is_admin": false, "content": "guestbook message b", "date": "2015-11-13 03:29:26.808801", "user_info": "None", "greeting_id": 4522291325042688, "updated_by": "", "updated_date": "2015-11-13 03:29:26.808804", "guestbook_name": "default_guestbook"}, {"is_admin": false, "content": "guestbook message b", "date": "2015-11-13 03:29:26.807145", "user_info": "None", "greeting_id": 6721314580594688, "updated_by": "", "updated_date": "2015-11-13 03:29:26.807150", "guestbook_name": "default_guestbook"}, {"is_admin": false, "content": "guestbook message b", "date": "2015-11-13 03:29:03.829938", "user_info": "None", "greeting_id": 5595414673752064, "updated_by": "", "updated_date": "2015-11-13 03:29:03.829941", "guestbook_name": "default_guestbook"}, {"is_admin": false, "content": "guestbook message b", "date": "2015-11-13 03:29:03.828506", "user_info": "None", "greeting_id": 6158364627173376, "updated_by": "", "updated_date": "2015-11-13 03:29:03.828510", "guestbook_name": "default_guestbook"}, {"is_admin": false, "content": "guestbook message b", "date": "2015-11-13 03:27:31.930525", "user_info": "None", "greeting_id": 5032464720330752, "updated_by": "", "updated_date": "2015-11-13 03:27:31.930545", "guestbook_name": "default_guestbook"}, {"is_admin": false, "content": "guestbook message b", "date": "2015-11-13 03:27:31.780663", "user_info": "None", "greeting_id": 6439839603884032, "updated_by": "", "updated_date": "2015-11-13 03:27:31.780669", "guestbook_name": "default_guestbook"}, {"is_admin": false, "content": "guestbook message b", "date": "2015-11-13 03:27:10.486645", "user_info": "None", "greeting_id": 5313939697041408, "updated_by": "", "updated_date": "2015-11-13 03:27:10.486651", "guestbook_name": "default_guestbook"}, {"is_admin": false, "content": "guestbook message b", "date": "2015-11-13 03:27:10.304004", "user_info": "None", "greeting_id": 5876889650462720, "updated_by": "", "updated_date": "2015-11-13 03:27:10.304020", "guestbook_name": "default_guestbook"}, {"is_admin": false, "content": "guestbook message b", "date": "2015-11-13 03:25:41.710036", "user_info": "None", "greeting_id": 4750989743620096, "updated_by": "", "updated_date": "2015-11-13 03:25:41.710040", "guestbook_name": "default_guestbook"}, {"is_admin": false, "content": "guestbook message b", "date": "2015-11-13 03:25:41.708163", "user_info": "None", "greeting_id": 6580577092239360, "updated_by": "", "updated_date": "2015-11-13 03:25:41.708169", "guestbook_name": "default_guestbook"}
			];

			this.server.respondWith([200, {'Content-Type': 'application/json'},
				json.stringify(results)]);

			guestbookstore.getGreetings().then(deferred.getTestCallback(function(posts) {
				doh.is(expected, posts);
			}));

			this.server.respond();
			return deferred;
		}),
		testAddGreeting: {

			setUp: function() {
				this.handles = [];
			},
			tearDown: function() {
				array.forEach(this.handles, function(handle) {
					handle.remove();
				}, this);
			},
			runTest: sinon.test(function() {

				var deferred = new doh.Deferred(),
					guestbookName = "default_guestbook";
				guestbookstore = new GuestbookStore({"guestbookName": guestbookName});
				addSpy = sinon.spy();
				this.handles.push(topic.subscribe('/api/guestbook/default_guestbook/greeting/', addSpy));
				guestbookstore.addGreeting('guestbook message c').then(deferred.getTestCallback(function(result) {
					doh.is(addSpy.callCount, 0);
				}));
				this.server.respondWith([204, {'Content-Type': 'application/json'}, '']);
				this.server.respond();
				return deferred;
			})
		},
		testAddGreetingFalse: {

			setUp: function() {
				this.handles = [];
			},
			tearDown: function() {
				array.forEach(this.handles, function(handle) {
					handle.remove();
				}, this);
			},
			runTest: sinon.test(function() {

				var deferred = new doh.Deferred(),
					guestbookName = "default_guestbook";
				guestbookstore = new GuestbookStore({"guestbookName": guestbookName});
				addSpy = sinon.spy();
				this.handles.push(topic.subscribe('/api/guestbook/default_guestbook/greeting/', addSpy));
				guestbookstore.addGreeting('guestbook message c').then(deferred.getTestCallback(function(result) {

				}),
				deferred.getTestCallback(function(error) {
					doh.is(error.response.status, 404);
				}));
				this.server.respondWith([404, {'Content-Type': 'application/json'}, '']);
				this.server.respond();
				return deferred;
			})
		},
		testAddGreetingInvalid: {

			setUp: function() {
				this.handles = [];
			},
			tearDown: function() {
				array.forEach(this.handles, function(handle) {
					handle.remove();
				}, this);
			},
			runTest: sinon.test(function() {

				var deferred = new doh.Deferred(),
					guestbookName = "default_guestbook";
				guestbookstore = new GuestbookStore({"guestbookName": guestbookName});
				addSpy = sinon.spy();
				this.handles.push(topic.subscribe('/api/guestbook/default_guestbook/greeting/', addSpy));
				guestbookstore.addGreeting('guestbook message c').then(deferred.getTestCallback(function(result) {

				}),
				deferred.getTestCallback(function(error) {
					doh.is(error.response.status, 400);
				}));
				this.server.respondWith([400, {'Content-Type': 'application/json'}, '']);
				this.server.respond();
				return deferred;
			})
		},
		testUpdateGreeting: {

			setUp: function() {
				this.handles = [];
			},
			tearDown: function() {
				array.forEach(this.handles, function(handle) {
					handle.remove();
				}, this);
			},
			runTest: sinon.test(function() {
				var deferred = new doh.Deferred(),
					guestbookName = "default_guestbook";
				guestbookstore = new GuestbookStore({"guestbookName": guestbookName});
				updateSpy = sinon.spy();
				this.handles.push(topic.subscribe('/api/guestbook/default_guestbook/greeting/5225978766819328', updateSpy));
				//console.log(putSpy);
				guestbookstore.updateGreeting(5225978766819328,'guestbook message b', guestbookName).then(deferred.getTestCallback(function(error) {
					doh.is(updateSpy.callCount, 0);
				}));
				this.server.respondWith([204, {'Content-Type': 'application/json'}, '']);
				this.server.respond();
				return deferred;
			})
		},
		testUpdateGreetingFalse: {

			setUp: function() {
				this.handles = [];
			},
			tearDown: function() {
				array.forEach(this.handles, function(handle) {
					handle.remove();
				}, this);
			},
			runTest: sinon.test(function() {
				var deferred = new doh.Deferred(),
					guestbookName = "default_guestbook";
				guestbookstore = new GuestbookStore({"guestbookName": guestbookName});
				updateSpy = sinon.spy();
				this.handles.push(topic.subscribe('/api/guestbook/default_guestbook/greeting/5225978766819328', updateSpy));
				//console.log(putSpy);
				guestbookstore.updateGreeting(5225978766819328,'guestbook message b', guestbookName).then(deferred.getTestCallback(function(result) {

				}),
				deferred.getTestCallback(function(error) {
					doh.is(error.response.status, 404);
				}));
				this.server.respondWith([404, {'Content-Type': 'application/json'}, '']);
				this.server.respond();
				return deferred;
			})
		},
		testUpdateGreetingInvalid: {

			setUp: function() {
				this.handles = [];
			},
			tearDown: function() {
				array.forEach(this.handles, function(handle) {
					handle.remove();
				}, this);
			},
			runTest: sinon.test(function() {
				var deferred = new doh.Deferred(),
					guestbookName = "default_guestbook";
				guestbookstore = new GuestbookStore({"guestbookName": guestbookName});
				updateSpy = sinon.spy();
				this.handles.push(topic.subscribe('/api/guestbook/default_guestbook/greeting/5225978766819328', updateSpy));
				//console.log(putSpy);
				guestbookstore.updateGreeting(5225978766819328,'guestbook message b', guestbookName).then(deferred.getTestCallback(function(result) {

				}),
				deferred.getTestCallback(function(error) {
					doh.is(error.response.status, 400);
				}));
				this.server.respondWith([400, {'Content-Type': 'application/json'}, '']);
				this.server.respond();
				return deferred;
			})
		},
		testGetGreetingDetail: {
			setUp: function() {
				this.handles = [];
			},
			tearDown: function() {
				array.forEach(this.handles, function(handle) {
					handle.remove();
				}, this);
			},
			runTest: sinon.test(function() {
				var deferred = new doh.Deferred(),
					guestbookName = "default_guestbook";
					guestbookstore = new GuestbookStore({"guestbookName": guestbookName});
					results =
						{"greeting_id": 6192449487634432, "updated_date": "2015-11-13 03:59:51.118471", "content": "guestbook message b", "user_info": "None", "is_admin": false, "updated_by": "", "date": "2015-11-13 03:59:51.118464", "guestbook_name": "default_guestbook"}
					,
					expected =
						{"greeting_id": 6192449487634432, "updated_date": "2015-11-13 03:59:51.118471", "content": "guestbook message b", "user_info": "None", "is_admin": false, "updated_by": "", "date": "2015-11-13 03:59:51.118464", "guestbook_name": "default_guestbook"}
					,
					guestbookstore = new GuestbookStore({"guestbookName": guestbookName});
					detailSpy = sinon.spy();
					this.handles.push(topic.subscribe('/api/guestbook/default_guestbook/greeting/5225978766819328', detailSpy));
					//console.log(putSpy);
					guestbookstore.getGreetingDetail(5225978766819328, guestbookName).then(deferred.getTestCallback(function(result) {
						doh.is(expected, result);
					}));
					this.server.respondWith([200, {'Content-Type': 'application/json'}, json.stringify(results)]);
					this.server.respond();
					return deferred;
			})
		},
		testGetGreetingDetailFalse: {
			setUp: function() {
				this.handles = [];
			},
			tearDown: function() {
				array.forEach(this.handles, function(handle) {
					handle.remove();
				}, this);
			},
			runTest: sinon.test(function() {
				var deferred = new doh.Deferred(),
					guestbookName = "default_guestbook";
					guestbookstore = new GuestbookStore({"guestbookName": guestbookName});
					results =
						{"greeting_id": 6192449487634432, "updated_date": "2015-11-13 03:59:51.118471", "content": "guestbook message b", "user_info": "None", "is_admin": false, "updated_by": "", "date": "2015-11-13 03:59:51.118464", "guestbook_name": "default_guestbook"}
					,
					expected =
						{"greeting_id": 6192449487634432, "updated_date": "2015-11-13 03:59:51.118471", "content": "guestbook message b", "user_info": "None", "is_admin": false, "updated_by": "", "date": "2015-11-13 03:59:51.118464", "guestbook_name": "default_guestbook"}
					,
					guestbookstore = new GuestbookStore({"guestbookName": guestbookName});
					detailSpy = sinon.spy();
					this.handles.push(topic.subscribe('/api/guestbook/default_guestbook/greeting/5225978766819328', detailSpy));
					//console.log(putSpy);
					guestbookstore.getGreetingDetail(5225978766819328, guestbookName).then(deferred.getTestCallback(function(result) {

					}),
					deferred.getTestCallback(function(error) {
						doh.is(error.response.status, 404);
					}));
					this.server.respondWith([404, {'Content-Type': 'application/json'}, '']);
					this.server.respond();
					return deferred;
			})
		},
		testDeleteGreeting: {
			setUp: function() {
				this.handles = [];
			},
			tearDown: function() {
				array.forEach(this.handles, function(handle) {
					handle.remove();
				}, this);
			},
			runTest: sinon.test(function() {
				var deferred = new doh.Deferred(),
					guestbookName = "default_guestbook";
				guestbookstore = new GuestbookStore({"guestbookName": guestbookName});
				deleteSpy = sinon.spy();
				this.handles.push(topic.subscribe('/api/guestbook/default_guestbook/greeting/5225978766819328', deleteSpy));
				//console.log(putSpy);
				guestbookstore.deleteGreeting(5225978766819328, guestbookName).then(deferred.getTestCallback(function(result) {
					console.log(result);
					doh.is(detailSpy.callCount, 0);
				}));
				this.server.respondWith([204, {'Content-Type': 'application/json'}, '']);
				this.server.respond();
				return deferred;
			})
		},
		testDeleteGreetingFalse: {
			setUp: function() {
				this.handles = [];
			},
			tearDown: function() {
				array.forEach(this.handles, function(handle) {
					handle.remove();
				}, this);
			},
			runTest: sinon.test(function() {
				var deferred = new doh.Deferred(),
					guestbookName = "default_guestbook";
				guestbookstore = new GuestbookStore({"guestbookName": guestbookName});
				deleteSpy = sinon.spy();
				this.handles.push(topic.subscribe('/api/guestbook/default_guestbook/greeting/5225978766819328', deleteSpy));
				//console.log(putSpy);
				guestbookstore.deleteGreeting(5225978766819328, guestbookName).then(deferred.getTestCallback(function(result) {

				}),
				deferred.getTestCallback(function(error) {
					doh.is(error.response.status, 404);
				}));
				this.server.respondWith([404, {'Content-Type': 'application/json'}, '']);
				this.server.respond();
				return deferred;
			})
		}
	})
});
