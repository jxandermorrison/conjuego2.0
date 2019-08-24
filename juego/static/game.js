function refreshOptions() {
	$(".option").each(function() {
		let id = $(this).attr("id");


function refreshPage(language) {
	$("#guess").val("");
	$("#guess").prop("disabled", false);
	$("#guess").focus();

	$.getJSON(`/verbs/${language}`, function(result) {
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

	if (path === "/en") {
		language = "english";
	} else if (path === "/es") {
		language = "spanish";
	} else if (path === "/pt") {
		language = "portuguese";
	} else if (path === "/jp") {
		language = "japanese";
	}

	refreshPage(language);

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
			$("#continue").fadeIn(300);
		} else {
			$(".answer").removeClass("list-group-item-success");
			$(".answer").addClass("list-group-item-danger");
			$("#guess").val("");
			$("#guess").focus();
		}
	});

	$(document).on("keypress", function(e) {
		if (e.which === 13 && $("#continue").is(":visible")) {
			$("#continue").click();
		}
	});

	$("#continue").click(function(e) {
		refreshPage(language);
	});
});
