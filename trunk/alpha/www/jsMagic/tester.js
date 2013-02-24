
tester = {
		
		loadTextById: function(id) {
			var jqueryId = '#' + id;
			var data = $(jqueryId).val();
			return data;
		},
		
		loadSolutionTextById: function(id) {
			// DEPRECATED, use loadTextById instead
			return tester.loadTextById(id);
		},
		
		evalText: function(text){
			//http://stackoverflow.com/questions/1271516/executing-anonymous-functions-created-using-javascript-eval
			var a = new Function('arg1', 'arg2', text); 
			return a;
		},
		
		runTest: function(solutionTextAreaId, testTextAreaId){
			var solutionText = tester.loadTextById(solutionTextAreaId);
			// no var infront of this: has to be global
			arg1 = '1';
			solution = tester.evalText(solutionText, arg1); 
			
			var testText = tester.loadTextById(testTextAreaId);
			// no var infront of this: has to be global
			test = tester.evalText(testText);
			

			return test();
		},
		
		runTestByIndex: function(i){
			solutionId = sprintf('%010d_solution_textarea', i);
			testId = sprintf('%010d_task_textarea', i);
			return tester.runTest(solutionId, testId);
		}
}