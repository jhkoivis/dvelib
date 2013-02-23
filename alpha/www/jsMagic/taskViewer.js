

taskViewer = {
		
	setTextToTaskTextArea: function(text, i) {
		var textAreaId = sprintf('%010d_task_textarea', i);
		$('#' + textAreaId).text(text);
	},

	addTitleToForm: function(i, form) {
		var title = document.createElement('h1');
		title.innerHTML = 'Task ' + i;
		title.id = sprintf('%010d_task_title', i);
		title.name = title.id; 
		form.appendChild(title);
		return form;
	},
	
	addSolutionTitleToForm: function(i, form) {
		var title = document.createElement('h1');
		title.innerHTML = 'Solution for task ' + i;
		title.id = sprintf('%010d_solution_title', i);
		title.name = title.id; 
		form.appendChild(title);
		return form;
	},
	
	addTaskTextAreaToForm: function(i, form) {
		var area = document.createElement('textarea');
		area.id = sprintf('%010d_task_textarea', i);
		area.name = area.id; 
		area.rows=3;
		area.cols=100;
		form.appendChild(area);
		return form;
	},

	addSolutionTextAreaToForm: function(i, form) {
		var area = document.createElement('textarea');
		area.id = sprintf('%010d_solution_textarea', i);
		area.name = area.id; 
		form.appendChild(area);
		return form;
	},

	addRunTestButtonToForm: function(i, form) {
		var input = document.createElement('input');
		input.id = sprintf('%010d_runTestButton', i);
		input.name = input.id;
		input.value = 'Run Test';
		input.type = "submit";
		input.onclick = "alert('test');";
		form.appendChild(input);
		return form;
	},
	
	bindButtonSubmitToFunctionAndArgById: function(buttonId, func, arg) {
		$(buttonId).submit(function() {
    		alert('222');
    		//func(arg);
    		return false;
    	});
	},
	
	addSendSolutionButtonToForm: function() {

	},

	createForm: function(i) {
		var form = document.createElement('form');
		form.id = sprintf('%010d_form', i);
		form.name = form.id; 
		form.action = "";

		form = taskViewer.addTitleToForm(i, form);
		form = taskViewer.addTaskTextAreaToForm(i, form);
		form = taskViewer.addSolutionTitleToForm(i, form);
		form = taskViewer.addSolutionTextAreaToForm(i, form);
		form = taskViewer.addRunTestButtonToForm(i, form);
		return form;	
	}
}



