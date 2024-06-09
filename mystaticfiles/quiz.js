document.addEventListener('DOMContentLoaded', (event) => {

    // Get the protocol of the current window
    const protocol = window.location.protocol === 'https:' ? 'wss://' : 'ws://';

    // Construct the WebSocket URL
    //has to match with:                wss://ppg-quiz-site-265ccf6f2c38.herokuapp.com/wss/quiz/Art/
    const quizSocket = new WebSocket(protocol + window.location.host + '/ws/quiz/' + quizTitle + '/' + sessionId + '/');


    //Get all HTML containers we need to manipulate
    const current_question_num_element = document.getElementById('current-question');
    const current_quiz_type_element = document.getElementById('quiz-type');
    const question_text_element = document.getElementById('question-text');
    const answers_ul_element = document.getElementById('answers-list');
    const user_ul_element = document.getElementById('user_list');
    const numOfUsers_element = document.getElementById('numOfUsers');
    //Difficulty rating element
    

    const timer_element = document.getElementById('timer-count');
    const timer_div_element = document.getElementById('timer');

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
            console.log("user picked an answer");
            handleUserSelection(data.username);
        }

        if (data.type === 'quiz_end') {
            console.log("caught the quiz end message");
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
            li.setAttribute("id", `username-${user.username}`);
            li.innerText = `${user.username}: ${user.score}`;
            user_ul_element.appendChild(li);
        });
    }

    function handleUserSelection(username) {
        const usernameElement = document.getElementById(`username-${username}`);
        if (usernameElement) {
            usernameElement.classList.add('chosen');
        }
    }

    function endQuiz(final_scores) {
        clearInterval(timer);
        timer_div_element.innerText = '';
        question_text_element.innerText = 'Quiz Finished!';
        answers_ul_element.innerHTML = '';

        final_scores.forEach((user) => {
            const li = document.createElement('li');
            li.innerText = `${user.username}: ${user.score}`;
            answers_ul_element.appendChild(li);
        });
    }
});
