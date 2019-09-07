$.fn.clicktoggle = function(a, b) {
    return this.each(function() {
        var clicked = false;
        $(this).click(function() {
            if (clicked) {
                clicked = false;
                return b.apply(this, arguments);
            }
            clicked = true;
            return a.apply(this, arguments);
        });
    });
};

var timerInterval;

let options = {
	"subject": [],
	"mood": [],
	"tense": []
};

function setProgress(correct, missed) {
	correct = Math.round(correct * 10) / 10;
	missed = Math.round(missed * 10) / 10;
	if (correct == 0 && missed == 0) {
		$("#option-score").text("");
	} else {
		$("#option-score").text(correct + "%")
	}
	correct = correct.toString();
	missed = missed.toString();
	$("#progress-success").css("width", correct + "%");
	$("#progress-danger").css("width", missed + "%");
	$("#progress-success").prop("aria-valuenow", correct);
	$("#progress-danger").prop("aria-valuenow", missed);
}

function showResultsModal() {
	let score = $("#option-score").text();
	$("#progress-report").text(score);
	$("#progress-modal").modal("show");
}
	

function startTimer(duration) {
	var start = Date.now(),
		diff,
		minutes,
		seconds;

	function timer() {
		diff = duration - (((Date.now() - start) / 1000) | 0);

		minutes = (diff / 60) | 0;
		seconds = (diff % 60) | 0;

		if (minutes == 0 && seconds == 0) {
			clearInterval(timerInterval);
			showResultsModal();
		}

		minutes = minutes < 10 ? "0" + minutes : minutes;
		seconds = seconds < 10 ? "0" + seconds : seconds;

		$("#option-clock").text(minutes + ":" + seconds);

		if (diff <= 0) {
			start = Date.now() + 1000;
		}
	}
	timer();
	let timerInterval = setInterval(timer, 1000);
	return timerInterval;
}

function addOption(array, item) {
	if (!(array.includes(item))) {
		array.push(item);
	}
}

function removeOption(array, item) {
	let index = array.indexOf(item);
	if (index > -1) {
		array.splice(index, 1);
	}
}

function refreshOptions() {
	$(".option").each(function() {
		let id = $(this).attr("id");
		if (localStorage.getItem(id) === null) {
			localStorage[id] = true;
		}
		var target = $(this).next("label").text();
		if (target !== "I") {
			target = target.toLowerCase();
		}
		if (localStorage.getItem(id) === "true") {
			$(this).prop("checked", true);
			if ($(this).hasClass("subject")) { 
				addOption(options.subject, target);
			}
			else if ($(this).hasClass("mood")) {
				addOption(options.mood, target);
			}
			else if ($(this).hasClass("tense")) {
				addOption(options.tense, target);
			}
		} else {
			$(this).prop("checked", false);
			if ($(this).hasClass("subject")) {
				removeOption(options.subject, target);
			}
			else if ($(this).hasClass("mood")) {
				removeOption(options.mood, target);
			}
			else if ($(this).hasClass("tense")) {
				removeOption(options.tense, target);
			}
		}
	});
}

function refreshPage(language, options) {
	$("#guess").val("");
	$("#guess").prop("disabled", false);
	$("#guess").focus();
	$("#submit").prop("disabled", false)

	$.getJSON(`/verbs/${language}`, encodeURIComponent(JSON.stringify(options)), function(result) {
		let target_mood, target_tense;
		if (result.browser_language == "pt") {
			target_mood = "pt_mood";
			target_tense = "pt_tense";
		} else if (result.browser_language == "es") {
			target_mood = "es_mood";
			target_tense = "es_tense";
		} else {
			target_mood = "en_mood";
			target_tense = "en_tense";
		}
		$("#subject").text(result.subject);
		$("#infinitive").text(result.infinitive);
		$("#mood").text(result[target_mood]);
		$("#tense").text(result[target_tense]);

		$("#answer-box").hide();
		$("#continue").hide();

		if (language === "english")
			$("#answer").text(`${result.subject} ${result.answer}`);
		else
			$("#answer").text(result.answer);

		if (language === "japanese") {
			$(".jp").remove();
			$(".answer-list").append(`<li class="list-group-item jp"><span id="kana">${result.kana}</span></li>`);
			$(".answer-list").append(`<li class="list-group-item jp"><span id="romaji">${result.romaji}</span></li>`);
		}
	});
}


$(document).ready(function() {
	let language;
	let browser_language = window.navigator.language.substring(0,2);
	let path = window.location.pathname;

	let right = 0;
	let missed = 0;

	refreshOptions();

	if (path === "/en") {
		language = "english";
	} else if (path === "/es") {
		language = "spanish";
	} else if (path === "/pt") {
		language = "portuguese";
	} else if (path === "/jp") {
		language = "japanese";
	}

	console.log(browser_language);

	refreshPage(language, options);

	$("#submission").submit(function(e) {
		e.preventDefault();
		let guess = $("#guess").val().toLowerCase();
		let correct = $("#answer").text().toLowerCase();
		let subject = $("#subject").text().toLowerCase();
		let infinitive = $("#infinitive").text().toLowerCase();

		$("#answer-box").fadeIn(500);
		if (path === "/jp") {
			var sl = "ja";
		} else {
			var sl = path.replace("/", "");
		}
		var tl = "en"; // switch out
		$("#translate").attr("href", `https://translate.google.com/#view=home&op=translate&sl=${sl}&tl=${tl}&text=${infinitive}`);
		if (guess === correct || (language !== "english" && ((guess === `${subject} ${correct}`) || (guess === correct)))) {
			$(".answer").removeClass("list-group-item-danger");
			$(".answer").addClass("list-group-item-success");
			$("#guess").prop("disabled", true);
			right++;
			$("#continue").fadeIn(300);
			$("#submit").prop("disabled", true)
		} else {
			$(".answer").removeClass("list-group-item-success");
			$(".answer").addClass("list-group-item-danger");
			$("#guess").val("");
			$("#guess").focus();
			missed++;
		}
		
		var right_perc = (right / (right + missed)) * 100
		var missed_perc = (missed / (right + missed)) * 100
		setProgress(right_perc, missed_perc);
	});

	$(document).on("keypress", function(e) {
		if (e.which === 13 && $("#continue").is(":visible")) {
			$("#continue").click();
		}
	});

	$("#continue").click(function(e) {
		refreshPage(language, options);
	});

	$("#save").click(function(e) {
		refreshOptions();
		refreshPage(language, options);
		$(".modal").modal("hide");
		setProgress(0, 0);
	});

	$(".option").change(function() {
		if ($("input.subject")[0]) {
			if ($("input.subject:checked").length === 0) {
				$(this).prop("checked", true);
			}
		}
		if ($("input.mood:checked").length === 0) {
			$(this).prop("checked", true);
		}
		if ($("input.tense:checked").length === 0) {
			$(this).prop("checked", true);
		}
		let id = $(this).attr("id");
		localStorage[id] = $(this).is(":checked");
		refreshOptions();
	});

	$("#start-timer").clicktoggle(function() {
		let minutes = $("#countdown-minutes").val() * 60;
		timerInterval = startTimer(minutes);
		if (browser_language === "es")
			$("#start-timer").text("Detener");
		else if (browser_language === "pt")
			$("#start-timer").text("Parar");
		else
			$("#start-timer").text("Stop Timer");
		$("#countdown-minutes").prop("disabled", true);
		setProgress(0, 0);
		right = 0;
		missed = 0;
		refreshPage(language, options);
		$("#option-clock").addClass("clock");
	}, function () {
		clearInterval(timerInterval);
		setProgress(0, 0);
		if (browser_language === "es" || browser_language === "pt")
			$("#start-timer").text("Iniciar");
		else
			$("#start-timer").text("Start Timer");
		$("#countdown-minutes").prop("disabled", false);
		$("#option-clock").text("");
		$("#option-clock").removeClass("clock");
	});

	$("#return-to-practice").click(function() {
		$("#start-timer").click();
	});

	$("#play-again").click(function() {
		$("#start-timer").click();
		$("#start-timer").click();
	});
});
