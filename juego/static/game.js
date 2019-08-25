let options = {
	"subject": [],
	"mood": [],
	"tense": []
};

function refreshOptions() {
	$(".option").each(function() {
		let id = $(this).attr("id");
		if (localStorage.getItem(id) === null) {
			localStorage[id] = true;
		}
		var target = $(this).next("label").text().toLowerCase();
		if (localStorage.getItem(id) === "true") {
			$(this).prop("checked", true);
			if ($(this).hasClass("subject")) { 
				if (!(options.subject.includes(target))) {
					options.subject.push(target);
				}
			}
			else if ($(this).hasClass("mood")) {
				if (!(options.mood.includes(target))) {
					options.mood.push(target);
				}
			}
			else if ($(this).hasClass("tense")) {
				if (!(options.tense.includes(target))) {
					options.tense.push(target);
				}
			}
		} else {
			$(this).prop("checked", false);
			if ($(this).hasClass("subject")) {
				var index = options.subject.indexOf(target);
				if (index > -1) {
					options.subject.splice(index, 1);
				}
			}
			else if ($(this).hasClass("mood")) {
				var index = options.mood.indexOf(target);
				if (index > -1) {
					options.mood.splice(index, 1);
				}
			}
			else if ($(this).hasClass("tense")) {
				var index = options.tense.indexOf(target);
				if (index > -1) {
					options.tense.splice(index, 1);
				}
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
		$("#subject").text(result.subject);
		$("#infinitive").text(result.infinitive);
		$("#mood").text(result.mood);
		$("#tense").text(result.tense);

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
	let browser_language = window.navigator.language;
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

		$("#progress-success").css("width", right_perc.toString() + "%");
		$("#progress-danger").css("width", missed_perc.toString() + "%");
		$("#progress-success").prop("aria-valuenow", right_perc.toString());
		$("#progress-danger").prop("aria-valuenow", missed_perc.toString());
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
		$("#progress-success").css("width", "0%");
		$("#progress-danger").css("width", "0%");
		$("#progress-success").prop("aria-valuenow", "0");
		$("#progress-danger").prop("aria-valuenow", "0");
	});

	$(".option").change(function() {
		let id = $(this).attr("id");
		localStorage[id] = $(this).is(":checked");
		refreshOptions();
	});
});
