/*  Author: Abelardo Pardo (<abelardo.pardo@sydney.edu.au>) */
/* Version: 150112 */
/* Variable to allow for UID set by other means (additional code needed) */
var given_uid = '';
function dynsite_send_data(s, v, o) {
    var data = {}
    /* If loading locally, skip the logging */
    if (location.protocol == 'file:') {
	// console.log('SEND:' + document.location.pathname + ',' + 
        //             DOCUMENTATION_OPTIONS.CONTEXT + ',' + v + ',' + JSON.stringify(o));
	return;
    }

    if (DOCUMENTATION_OPTIONS.DATA_CAPTURE_URL != '') {
        data[DOCUMENTATION_OPTIONS.DATA_CAPTURE_CONTEXT_NAME] = DOCUMENTATION_OPTIONS.CONTEXT;
        data[DOCUMENTATION_OPTIONS.DATA_CAPTURE_SUBJECT_NAME] = s;
        data[DOCUMENTATION_OPTIONS.DATA_CAPTURE_VERB_NAME] = v;
        data[DOCUMENTATION_OPTIONS.DATA_CAPTURE_OBJECT_NAME] = JSON.stringify(o);
        $.ajax({
	    'type': DOCUMENTATION_OPTIONS.DATA_CAPTURE_METHOD,
	    'url': DOCUMENTATION_OPTIONS.DATA_CAPTURE_URL,
	    'data': data
        });
    }
}
/*****  duration form submission **** */
$(document).ready(function() {
    function init() {
	/* This is button. Parent is the form element */
	var form_el = $(this).parent();
        var ok_icon = form_el.parent().children("img");

	$(this).click(function(e){
	    e.preventDefault();
	    data = {};
	    data[form_el.find('input[name = "duration-id"]').val()] =
		 form_el.find('select[name = "duration-value"]').val();
	    dynsite_send_data(given_uid, "activity-duration", data);
	    form_el.hide()
	    ok_icon.show()
	    return false;  //stop the actual form post !important!
	});
    }
    $(".reauthoring_duration_submit").each(init)
});
/*****  Generic form submission **** */
$(document).ready(function() {
    function init() {
	/* This is button. Parent is the form element */
	var form_el = $(this).closest('form');
        var ok_icon = form_el.parent().children("img");

	$(this).click(function(e){
	    e.preventDefault();
	    data = {};
	    /* This is the default event name */
	    event_name = "form-submit";
	    /* Loop over the input elements in the form */
	    form_el.find('*').filter(':input').each(function(){
		if (this.name == "") {
		    return;
                }
		/* And this to catch the event name from within the form */
		if (this.name == "event-name") {
		    event_name = this.value;
		    return;
		}
		/* Accumulate the rest of input fields */
		data[this.name] = this.value;
	    });
	    /* Store also the URL */
	    data['url'] = document.URL;
	    /* Send! */
	    dynsite_send_data(given_uid, event_name, data);
	    form_el.hide()
	    ok_icon.show()
	    return false;  //stop the actual form post !important!
	});
    }
    $(".reauthoring_submit").each(init)
});
/***** Expand collapse of sections *****/
$(document).ready(function (){
    function init(){
	// get header & section, and add static classes
	var header = $(this);
	var section = header.parent();
	header.addClass("html-toggle-button");
	
	// helper to test if url hash is within this section
	function contains_hash(){
	    var hash = document.location.hash;
	    return hash && (section[0].id == hash.substr(1) ||
			    section.find(hash.replace(/\./g,"\\.")).length>0);
	}
	
	// helper to control toggle state
	function set_state(expanded, track) {
	    if (expanded) {
		section.addClass("expanded").removeClass("collapsed");
		section.children().show();
		event_name = "expand";
	    } else {
		section.addClass("collapsed").removeClass("expanded");
		section.children().hide();
		/* for :ref: span tag */
		section.children("span:first-child:empty").show();
		header.show();
		event_name = "collapse";
	    }

	    if (track && DOCUMENTATION_OPTIONS.DATA_CAPTURE_URL) {
		data = {};
		data["page"] = document.URL.replace(/#.*$/, "");
		data[section.attr("id")] = event_name;
		dynsite_send_data(given_uid, 'activity-collapse-expand', data);
	    }
	}
	
	// initialize state
	set_state(section.hasClass("expanded") || contains_hash(),
		  contains_hash());
	
	// bind toggle callback
	header.click(function (){
	    set_state(!section.hasClass("expanded"), true);
	    $(window).trigger('cloud-section-toggled', section[0]);
	});
	
	// open section if user jumps to it from w/in page
	$(window).bind("hashchange", function () {
            if(contains_hash()) set_state(true, true);
	});
    }

    // Apply to activity with section attribute
    $(".activity.section > h2, .activity.section > h3, .activity.section > h4, .activity.section > h5, .activity.section > h6").each(init);

    // Apply to chapter sections!
    $("div.chapter-with-expand > div.section > h1, div.chapter-with-expand > div.section > h2, div.chapter-with-expand > div.section > h3, div.chapter-with-expand > div.section > h4, div.chapter-with-expand > div.section > h5, div.chapter-with-expand > div.section > h6").each(init);
});
/***** Embedded MCQ *****/
function grade_mcq(div_el) {
    /* Ordered list element with the answer */
    var answer_list = div_el.find("form > ol.eqt-answer-list");

    /* Detect no answer */
    var answer = -1

    /* Get all the answer elements */
    /* var listitems = div_el.find("form > ol.eqt-answer-list > li");*/
    var listitems = answer_list[0].getElementsByTagName("li");
    /* Loop over input element of each answer */
    for (i = 0, max = listitems.length; i < max; i++) {
	var li = listitems.item(i);
	/* Get the input */
	var inp = li.getElementsByTagName('input');
	var tochange;

	/* If not checked, keep looping */
	if (! inp[0].checked ) {
	    continue;
	}

	/* Select which image to show depending on the correct/incorrect mark */
	if (inp[0].value == "C") {
	    tochange = li.getElementsByClassName('correct_icon');
	    answer = 1;
	} else {
	    tochange = li.getElementsByClassName('incorrect_icon');
	    answer = 0;
	}
	
	/* Show the icon */
	tochange[0].style.opacity = "1";
	break;
    }

    return answer;
}

function grade_fib(div_el) {
    var inside_div = div_el.find("form > div.reauthoring_embedded_quiz-fib-answer");

    /* Find input element */ 
    var qval = inside_div.find("input[name = 'question']")[0].value;
    var aval = inside_div.find("input[name = 'solution']")[0].getAttribute("value");
    
    /* Empty answer prompts no action */
    if (qval == "") {
	return -1;
    }

    if (qval == aval) {
	tochange = inside_div[0].getElementsByClassName('correct_icon');
	answer = 1;
    } else {
	tochange = inside_div[0].getElementsByClassName('incorrect_icon');
	answer = 0;
    }

    /* Show the icon */
    tochange[0].style.opacity = "1";
    return answer;
}

function grade() {
    /* Get the div element to process from above */
    var div_el = $(this).parent().parent();
    
    div_id = div_el[0].getAttribute('class');
    if (div_id.substring(div_id.length - 4, div_id.length) == "-fib") {
	answer = grade_fib(div_el);
    } else {
	answer = grade_mcq(div_el);
    }

    /* Grade button pushed with no answer given. Finish */
    if (answer == -1) {
	return;
    }

    // Send the "embedded-question-grade" event
    data = {};
    data[div_el.attr('id')] = answer;
    dynsite_send_data(given_uid, 'embedded-question', data);

    /* Change the visibility of the buttons */
    var bts = this.parentNode.getElementsByTagName('input');
    bts[0].style.display="none";
    bts[1].style.display="inline";
    bts[2].style.display="inline";
};

function again_mcq(div_el) {
    /* Ordered list element with the answer */
    var answer_list = div_el.find("form > ol.eqt-answer-list");

    /* Get all the img elements correct and incorrect */
    var listitems = answer_list[0].getElementsByClassName('correct_icon');
    /* Loop over the correct img elements of the answer */
    for (i = 0, max = listitems.length; i < max; i++) {
	listitems[i].style.opacity = "0";
    }
    listitems = answer_list[0].getElementsByClassName('incorrect_icon');
    /* Loop over the incorrect img elements of the answer */
    for (i = 0, max = listitems.length; i < max; i++) {
	listitems[i].style.opacity = "0";
    }

    var radios = answer_list[0].getElementsByTagName('input');
    for (i = 0, max = radios.length; i < max; i++) {
	radios[i].checked = false;
    }

}

function again_fib(div_el) {
    var inside_div = div_el.find("form > div.reauthoring_embedded_quiz-fib-answer");

    /* Find input element */ 
    inside_div.find("input[name = 'question']")[0].value = "";
    inside_div.find("img").css('opacity', '0');
}

function again() {
    /* Get the form element to process from above */
    var div_el = $(this).parent().parent();

    div_id = div_el[0].getAttribute('class');
    if (div_id.substring(div_id.length - 4, div_id.length) == "-fib") {
	again_fib(div_el);
    } else {
	again_mcq(div_el);
    }
    
    /* And restore the view in which only the grade button is visible */
    var bts = this.parentNode.getElementsByTagName('input');
    bts[0].style.display="inline";
    bts[1].style.display="none";
    bts[2].style.display="none";
}

function solutions_mcq(div_el) {
    /* Ordered list element with the answer */
    var answer_list = div_el.find("form > ol.eqt-answer-list");

    /* Get all the answer elements */
    var listitems = answer_list[0].getElementsByTagName("li");

    /* Loop over input element of each answer */
    for (i = 0, max = listitems.length; i < max; i++) {
	/* Get the input */
	var inp = listitems[i].getElementsByTagName('input');

	if (inp[0].value == "C") {
	    tochange = listitems[i].getElementsByClassName('correct_icon');
	} else {
	    tochange = listitems[i].getElementsByClassName('incorrect_icon');
	}

	/* Show the icon */
	tochange[0].style.opacity = "1";
    }
}

function solutions_fib(div_el) {
    /* Find answer value and set it to the value of the question field */
    var inside_div = div_el.find("form > div.reauthoring_embedded_quiz-fib-answer");
    var aval = inside_div.find("input[name = 'solution']")[0].getAttribute("value");
    inside_div.find("input[name = 'question']")[0].value = aval;
    inside_div.find("img").css('opacity', '0');
}

function solutions() {
    /* Get the div element to process from above */
    var div_el = $(this).parent().parent();

    div_id = div_el[0].getAttribute('class');
    if (div_id.substring(div_id.length - 4, div_id.length) == "-fib") {
	solutions_fib(div_el);
    } else {
	solutions_mcq(div_el);
    }
    
    // Send the "embedded-question-again" event
    data = {};
    data[div_el.attr('id')] = "-1";
    dynsite_send_data(given_uid, 'embedded-question', data);
}

$(document).ready(function () {
    /* Get the buttons to execute the correct functions when clicked */
    var hc = $('.reauthoring_embedded_quiz_buttons');
    hc.find('input:nth-child(1)').click(grade);
    hc.find('input:nth-child(1)').css('display', 'inline');
    hc.find('input:nth-child(2)').click(again);
    hc.find('input:nth-child(3)').click(solutions);

    /* Background of the list and the correct/incorrect icons */
    hc = $('.reauthoring_embedded_quiz_questions');
    hc.find('li').css('background',
		      'none no-repeat 0 0').css('marginLeft', '2em');
    hc.find('ol').css('listStyleType', 'upper-alpha');
    hc.find('ul').css('listStyleType', 'upper-alpha');

    /* MCQ */
    $('.reauthoring_embedded_quiz .correct_icon').css('marginLeft',
    			'-43px').css('marginRight', '43px');
    $('.reauthoring_embedded_quiz .incorrect_icon').css('marginLeft',
    				  '-66px').css('marginRight', '23px');
    /* FIB */
    $('.reauthoring_embedded_quiz-fib .incorrect_icon').css('marginLeft',
    				  '-23px');
});
/* Page now records an event upon loading */
$(document).ready(function() {
    data = {};
    data['url'] = document.URL;
    dynsite_send_data(given_uid, "resource-view", data);
});
