document.addEventListener('DOMContentLoaded', (event) => {
    const pathParts = window.location.pathname.split('/');
    const quizTitle = pathParts[pathParts.length - 2];
    const quizSocket = new WebSocket('ws://' + window.location.host + '/ws/quiz/' + quizTitle + '/');

    const current_question_num_element = document.getElementById('current-question');
    const current_quiz_type_element = document.getElementById('quiz-type');
    const question_text_element = document.getElementById('question-text');
    const answers_ul_element = document.getElementById('answers-list');
    const user_ul_element = document.getElementById('user_list');
    const numOfUsers_element = document.getElementById('numOfUsers');
    const timer_element = document.getElementById('timer-count');

    let timer;
    let timeLeft;

    quizSocket.onmessage = function (e) {
        const data = JSON.parse(e.data);

        if (data.type === 'game_state') {
            const gameState = data.game_state;
            updateGameState(gameState);
        }

        if (data.type === 'user_list') {
            updateUserList(data.users);
        }

        if (data.type === 'user_selection') {
            handleUserSelection(data.username);
        }

        if (data.type === 'quiz_end') {
            endQuiz(data.final_scores);
        }
    };

    function updateGameState(gameState) {
        current_question_num_element.innerText = gameState.current_question + 1;
        current_quiz_type_element.innerText = gameState.quizType;
        question_text_element.innerText = gameState.question;
        numOfUsers_element.innerText = gameState.numOfUsers;

        answers_ul_element.innerHTML = '';
        gameState.answers.forEach((answer) => {
            const li = document.createElement('li');
            li.innerText = answer.text;
            li.classList.add('unselected');
            li.addEventListener('click', function clickHandler() {
                if (this.classList.contains('unselected')) {
                    answers_ul_element.querySelectorAll('li').forEach(item => {
                        item.classList.remove('unselected');
                    });
                    this.classList.add('toggled');
                    quizSocket.send(JSON.stringify({
                        'type': 'answer_selected',
                        'answer_id': answer.id,
                    }));
                }
            });
            answers_ul_element.appendChild(li);
        });

        startTimer(15); // Start the timer for 15 seconds
    }

    function startTimer(seconds) {
        clearInterval(timer);
        timeLeft = seconds;
        timer_element.innerText = timeLeft;
        timer = setInterval(() => {
            timeLeft -= 1;
            timer_element.innerText = timeLeft;
            if (timeLeft <= 0) {
                clearInterval(timer);
                quizSocket.send(JSON.stringify({
                    'type': 'timer_expired',
                }));
            }
        }, 1000);
    }

    function updateUserList(users) {
        user_ul_element.innerHTML = '';
        users.forEach((user) => {
            const li = document.createElement('li');
            li.innerText = `${user.username}: ${user.score}`;
            user_ul_element.appendChild(li);
        });
    }

    function handleUserSelection(username) {
        const user_li_element = document.querySelector(`#user_list li[data-username="${username}"]`);
        if (user_li_element) {
            user_li_element.classList.add('answered');
        }
    }

    function endQuiz(final_scores) {
        clearInterval(timer);
        question_text_element.innerText = 'Quiz Finished!';
        answers_ul_element.innerHTML = '';

        final_scores.forEach((user) => {
            const li = document.createElement('li');
            li.innerText = `${user.username}: ${user.score}`;
            user_ul_element.appendChild(li);
        });
    }
});
