$(document).ready(function() {
	let language;
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

	$("#guess").focus();

	$.getJSON(`/verbs/${language}`, function(result) {
		$("#subject").text(result.subject);
		$("#infinitive").text(result.infinitive);
		$("#mood").text(result.en_mood);
		$("#tense").text(result.en_tense);

		$("#answer-box").hide();
		$("#continue").hide();

		if (language === "english")
			$("#answer").text(`${result.subject} ${result.answer}`);
		else
			$("#answer").text(result.answer);

		if (language === "japanese") {
			$(".answer-list").append(`<li class="list-group-item"><span id="kana">${result.kana}</span></li>`);
			$(".answer-list").append(`<li class="list-group-item"><span id="romaji">${result.romaji}</span></li>`);
		}
	});

	$("#submission").submit(function(e) {
		e.preventDefault();
		let guess = $("#guess").val().toLowerCase();
		let correct = $("#answer").text().toLowerCase();
		let subject = $("#subject").text().toLowerCase();
		let infinitive = $("#infinitive").text().toLowerCase();

		$("#answer-box").fadeIn(500);
		var sl = path.replace("/", "")
		var tl = "en"
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
		console.log("MADE IT HERE");
	});
});
