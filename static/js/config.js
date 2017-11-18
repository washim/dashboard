var messages = function(title,body){
	var View2 = Backbone.View.extend({
		el: "#messages",
		render: function(){
			var that = this;
			$.ajax({
				url: "/static/resources/messages.html",
				success: function(data){
					var template = _.template(data);
					that.$el.html(template({"title":title,"body":body}));
				},
				cache: false
			});
		}
	});
	view2 = new View2();
	view2.render();
}

$(".btnCalculateLossProfit").click(function() {
	var symbol = $("#stocksymbol");
	var interval = $("#stockinterval");
	var confidence = $("#stockconfidenceinterval");
	var investment = $("#stockinvest");
	var start = $("#stockstartdt");
	var end = $("#stockenddt");
	
	if (investment.val() == "" || !$.isNumeric(investment.val())) {
		investment.addClass("form-error");
		return false;
	}
	
	$(this).attr("disabled","disabled");
	$("#loader1").removeClass("viewhide");
	
	investment.removeClass("form-error");
	
	var url = '/stocktolerance?symbol=' + symbol.val() + '&interval=' + interval.val() + '&confidence=' + confidence.val() + '&investment=' + investment.val() + '&start=' + start.val() + '&end=' + end.val()
	console.log(url);
	var Collection1 = Backbone.Collection.extend({
		url: url
	});
	
	var View1 = Backbone.View.extend({
		el: $("#stockstickers"),
		render: function(){
			var that = this;
			$.ajax({
				url: "/static/resources/view1.html",
				success: function(data){
					var template = _.template(data);
			        var collection1 = new Collection1();
			        collection1.fetch({
						success: function() {
							$("#messages").html("");
							$(".btnCalculateLossProfit").removeAttr("disabled");
							$("#loader1").addClass("viewhide");
							that.$el.html(template({rs1: collection1.models[0].attributes}));
						},
						error: function(){
							$(".btnCalculateLossProfit").removeAttr("disabled");
							$("#loader1").addClass("viewhide");
							messages("Alert","Please check whether you have enter correct stock price and investment.");
						}
					});
				},
				cache: false
			});
		}
	});
	
	var view1 = new View1();
	view1.render();
});