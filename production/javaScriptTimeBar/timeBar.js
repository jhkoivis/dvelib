


timeBar = {
		
		// Timer Bar - Version 1.3
		//
		// RELEASE INFO:
		//
		// Author: Juha Koivisto  (1.3)
		// V 1.3 - Changed to object oriented programming style
		//
		// Author: Brian Gosselin (up to 1.2)
		// V 1.2 - ADDED FUNCTIONALITY TO CONTROL WHEN YOU CLICK THE TIMERBAR.
		// V 1.1 - CHANGED THE action() FUNCTION SO HIDING THE BAR IS SELECTABLE.
		// V 1.0 - INTIAL RELEASE
		
		// THE FUNCTION BELOW CONTAINS THE ACTION(S) TAKEN ONCE BAR REACHES 100%.
		// IF NO ACTION IS DESIRED, TAKE EVERYTHING OUT FROM BETWEEN THE CURLY BRACES ({})
		// PRESENTLY, IT IS SET TO DO NOTHING, BUT CAN BE CHANGED EASILY.
		// TO CAUSE A REDIRECT TO ANOTHER PAGE, INSERT THE FOLLOWING LINE:
		// document.location.href="http://redirect_page.html";
		// JUST CHANGE THE ACTUAL URL OF COURSE :)

		loadedColor: 	'darkgray',
		unloadedColor:	'lightgray',
		borderColor:	'navy',
		barHeight:		15,
		barWidth:		300,
		waitTime:		10,
		
		// THE FUNCTION BELOW CONTAINS THE ACTION(S) TO TAKE PLACE IF THE USER
		// CLICKS THE TIMERBAR. THIS CAN BE USED TO CANCEL THE TIMERBAR.
		// IF YOU WISH NOTHING TO HAPPEN, SIMPLY REMOVE EVERYTHING BETWEEN THE CURLY BRACES.
		
		action: function()
		{
			timeBar.hidebar();
			alert(timeBar.waitTime+' seconds have elapsed.');
		},
		
		hidebar: function (){
			clearInterval(timeBar.Pid);
			if(timeBar.ns4) timeBar.PBouter.visibility="hide";
			else timeBar.PBouter.style.visibility="hidden";
		},
		
		clickBar: function(){
			timeBar.hidebar();
			alert('Timer cancelled.');
		},
			
		//*****************************************************//
		//**********  DO NOT EDIT BEYOND THIS POINT  **********//
		//*****************************************************//

		ns4: 		(document.layers)?true:false,
		ie4: 		(document.all)?true:false,
		loaded:		0,
		PBRouter:	0,
		PBDone:		0,
		Pid:		0,
		
		getBlocksize: function(){
			return (timeBar.barWidth-2)/timeBar.waitTime/10;
		},
		
		getBarTxt:	function(){
			var txt='';
			if(timeBar.ns4){
				txt+='<table border=0 cellpadding=0 cellspacing=0><tr><td>';
				txt+='<ilayer name="timeBar.PBouter" visibility="hide" height="'+timeBar.barHeight+'" width="'+timeBar.barWidth+'" onmouseup="timeBar.clickBar()">';
				txt+='<layer width="'+timeBar.barWidth+'" height="'+timeBar.barHeight+'" bgcolor="'+timeBar.borderColor+'" top="0" left="0"></layer>';
				txt+='<layer width="'+(timeBar.barWidth-2)+'" height="'+(timeBar.barHeight-2)+'" bgcolor="'+timeBar.unloadedColor+'" top="1" left="1"></layer>';
				txt+='<layer name="timeBar.PBdone" width="'+(timeBar.barWidth-2)+'" height="'+(timeBar.barHeight-2)+'" bgcolor="'+timeBar.loadedColor+'" top="1" left="1"></layer>';
				txt+='</ilayer>';
				txt+='</td></tr></table>';
			}else{
				txt+='<div id="timeBar.PBouter" onmouseup="timeBar.clickBar()" style="position:relative; visibility:hidden; background-color:'+timeBar.borderColor+'; width:'+timeBar.barWidth+'px; height:'+timeBar.barHeight+'px;">';
				txt+='<div style="position:absolute; top:1px; left:1px; width:'+(timeBar.barWidth-2)+'px; height:'+(timeBar.barHeight-2)+'px; background-color:'+timeBar.unloadedColor+'; font-size:1px;"></div>';
				txt+='<div id="timeBar.PBdone" style="position:absolute; top:1px; left:1px; width:0px; height:'+(timeBar.barHeight-2)+'px; background-color:'+timeBar.loadedColor+'; font-size:1px;"></div>';
				txt+='</div>';
			}
			return txt;
		},
		
		resizeEl:	function(id,t,r,b,l){
			if(timeBar.ns4){
				id.clip.left=l;
				id.clip.top=t;
				id.clip.right=r;
				id.clip.bottom=b;
			}else id.style.width=r+'px';
		},
		
		//THIS FUNCTION BY MIKE HALL OF BRAINJAR.COM
		findlayer: function(name,doc){
			var i,layer;
			for(i=0;i<doc.layers.length;i++){
				layer=doc.layers[i];
				if(layer.name==name)return layer;
				if(layer.document.layers.length>0) 
					if((layer=findlayer(name,layer.document))!=null)
						return layer;
			}
			return null;
		},
		
		progressBarInit: function(){
			timeBar.PBouter=(timeBar.ns4)?timeBar.findlayer('timeBar.PBouter',document):(timeBar.ie4)?document.all['timeBar.PBouter']:document.getElementById('timeBar.PBouter');
			timeBar.PBDone=(timeBar.ns4)?timeBar.PBouter.document.layers['timeBar.PBdone']:(timeBar.ie4)?document.all['timeBar.PBdone']:document.getElementById('timeBar.PBdone');
			timeBar.resizeEl(timeBar.PBDone,0,0,timeBar.barHeight-2,0);
			if(timeBar.ns4)timeBar.PBouter.visibility="show";
			else timeBar.PBouter.style.visibility="visible";
			timeBar.Pid=setInterval('timeBar.incrCount()',95);
		},
		
		incrCount: function(){
			timeBar.loaded++;
			if(timeBar.loaded<0) timeBar.loaded=0;
			if(timeBar.loaded>=timeBar.waitTime*10){
				clearInterval(timeBar.Pid);
				timeBar.loaded=timeBar.waitTime*10;
				setTimeout('timeBar.action()',100);
			}
			timeBar.resizeEl(timeBar.PBDone, 0, timeBar.getBlocksize()*timeBar.loaded, timeBar.barHeight-2, 0);
		},
		
		add:	function(){
			document.write(timeBar.getBarTxt());
			window.onload=timeBar.progressBarInit;
		}
}









