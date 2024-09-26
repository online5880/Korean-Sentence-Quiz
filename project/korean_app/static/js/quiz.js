$(document).ready(function() {
    var score = 0;
    var questionCount = 0;
    var totalQuestions = 10;
    var startTime;

    function loadNewQuiz() {
        $.get('/text-analysis/get_random_sentence/', function(data) {
            $('#sentence').text(data.sentence);
            $('#quiz-word').text(data.word);
            $('#correct-answer').val(data.pos);
            $('#user-answer').val('').focus();
            questionCount++;
            updateRemainingQuestions();
        });
    }

    function updateRemainingQuestions() {
        var remaining = totalQuestions - questionCount;
        $('#remaining-questions').text(remaining);
    }

    function checkAnswer() {
        var userAnswer = $('#user-answer').val().trim();
        var correctAnswer = $('#correct-answer').val();
        var sentence = $('#sentence').text();
        var targetWord = $('#quiz-word').text();
        var timeTaken = Math.floor((new Date() - startTime) / 1000);

        $.post('/text-analysis/check_answer/', {
            user_answer: userAnswer,
            correct_answer: correctAnswer,
            sentence: sentence,
            target_word: targetWord,
            time_taken: timeTaken,
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
        }, function(data) {
            if (data.is_correct) {
                $('#result').html(`정답입니다! "<span class="highlight correct">${data.target_word}</span>"는 <span class="highlight correct">${data.correct_answer}</span>입니다.`);
                score++;
            } else {
                $('#result').html(`틀렸습니다. "<span class="highlight">${data.target_word}</span>"는 <span class="highlight correct">${data.correct_answer}</span>입니다. (당신의 답변: <span class="incorrect">${data.user_answer}</span>)`);
            }
            $('#score').text(score);
            $('#remaining-questions').text(totalQuestions - questionCount);

            if (questionCount < totalQuestions) {
                loadNewQuiz();
            } else {
                endQuiz();
            }
        });
    }

    function endQuiz() {
        var endTime = new Date();
        var timeTaken = (endTime - startTime) / 1000;  // 초 단위로 계산

        $.post('/text-analysis/save_quiz_result/', {
            score: score,
            time_taken: timeTaken,
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
        }, function(data) {
            if (data.status === 'success') {
                window.location.href = '/text-analysis/results/';
            } else {
                alert('퀴즈 결과 저장에 실패했습니다.');
            }
        });
    }

    $('#check-answer').click(checkAnswer);
    
    $('#user-answer').keypress(function(e) {
        if (e.which == 13) {
            checkAnswer();
            return false;
        }
    });

    $('#toggle-pos-list').click(function() {
        $('#pos-list').toggleClass('hidden');
        $(this).text(function(i, text) {
            return text === "품사 목록 펼치기" ? "품사 목록 접기" : "품사 목록 펼치기";
        });
    });

    $('.info-icon').each(function() {
        $(this).wrap('<span class="tooltip"></span>');
        var tooltipText = $(this).attr('data-description');
        $(this).after('<span class="tooltiptext">' + tooltipText + '</span>');
        $(this).removeAttr('data-description');
    });

    $('.info-icon').click(function() {
        $(this).siblings('.pos-description').toggleClass('hidden');
    });

    startTime = new Date();  // 퀴즈 시작 시간 기록
    loadNewQuiz();
});