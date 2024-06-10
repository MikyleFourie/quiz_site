document.addEventListener('DOMContentLoaded', (event) => {

    // Get the protocol of the current window
    const protocol = window.location.protocol === 'https:' ? 'wss://' : 'ws://';

    // Construct the WebSocket URL
    //has to match with:                wss://ppg-quiz-site-265ccf6f2c38.herokuapp.com/wss/quiz/Art/
    const quizSocket = new WebSocket(protocol + window.location.host + '/ws/quiz/' + quizTitle + '/' + sessionId + '/');


    //Get all HTML containers we need to manipulate
    const current_question_num_element = document.getElementById('current-question');
    const current_quiz_type_element = document.getElementById('quiz-type');
    const current_ques_diff_element = document.getElementById('ques-diff');
    const question_text_element = document.getElementById('question-text');
    const answers_ul_element = document.getElementById('answers-list');
    const user_ul_element = document.getElementById('user_list');
    const numOfUsers_element = document.getElementById('numOfUsers');
    //Difficulty rating element
    

    // Get the HTML element for the timer count
    const timer_element = document.getElementById('timer-count');
    // Get the HTML element for the timer div
    const timer_div_element = document.getElementById('timer');

    // Variables for the timer and the time left
    let timer;
    let timeLeft;

    // Event listener for messages from the quiz socket
    quizSocket.onmessage = function (e) {
        const data = JSON.parse(e.data); // Parse the received data

        // Handle different types of messages
        if (data.type === 'game_state') {
            const gameState = data.game_state;
            updateGameState(gameState); // Update the game state
        }

        if (data.type === 'user_list') {
            updateUserList(data.users); // Update the user list
        }

        if (data.type === 'user_selection') {
            console.log("user picked an answer");
            handleUserSelection(data.username); // Handle user selection
        }

        if (data.type === 'quiz_end') {
            console.log("caught the quiz end message");
            endQuiz(data.final_scores); // Handle the end of the quiz
        }
    };

    // Function to update the game state
    function updateGameState(gameState) {
        // Update the current question number, quiz type, question text, and number of users
        current_question_num_element.innerText = gameState.current_question + 1;
        current_quiz_type_element.innerText = gameState.quizType;
        question_text_element.innerText = gameState.question;
        numOfUsers_element.innerText = gameState.numOfUsers;

        if (gameState.ques_diff == 1) {
            current_ques_diff_element.innerText = "Easy";
        } else if (gameState.ques_diff == 2) {
            current_ques_diff_element.innerText = "Intermediate";
        } else {
            current_ques_diff_element.innerText = "Hard";
        }
         

        // Clear the answers list
        answers_ul_element.innerHTML = '';
        // Populate the answers list
        gameState.answers.forEach((answer) => {
            const li = document.createElement('li');
            li.innerText = answer.text;
            li.classList.add('unselected');
            // Add click event listener for each answer
            li.addEventListener('click', function clickHandler() {
                if (this.classList.contains('unselected')) {
                    // Remove 'unselected' class from all answers and add 'toggled' class to the selected one
                    answers_ul_element.querySelectorAll('li').forEach(item => {
                        item.classList.remove('unselected');
                    });
                    this.classList.add('toggled');
                    // Send the selected answer ID to the server
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

    // Function to start the timer
    function startTimer(seconds) {
        clearInterval(timer); // Clear any existing timer
        timeLeft = seconds; // Set the time left
        timer_element.innerText = timeLeft; // Update the timer element
        timer = setInterval(() => { // Start a new interval
            timeLeft -= 1; // Decrease the time left by 1 second
            timer_element.innerText = timeLeft; // Update the timer element
            if (timeLeft <= 0) { // If the time is up
                clearInterval(timer); // Clear the timer
                quizSocket.send(JSON.stringify({
                    'type': 'timer_expired',
                })); // Notify the server that the timer expired
            }
        }, 1000);
    }

    // Function to update the user list
    function updateUserList(users) {
        user_ul_element.innerHTML = ''; // Clear the user list
        users.forEach((user) => {
            const li = document.createElement('li');
            li.setAttribute("id", `username-${user.username}`);
            li.innerText = `${user.username}: ${user.score}`;
            user_ul_element.appendChild(li); // Add each user to the list
        });
    }

    // Function to handle user selection
    function handleUserSelection(username) {
        const usernameElement = document.getElementById(`username-${username}`);
        if (usernameElement) {
            usernameElement.classList.add('chosen'); // Highlight the selected user
        }
    }

    // Function to end the quiz
    function endQuiz(final_scores) {
        clearInterval(timer); // Clear the timer
        timer_div_element.innerText = ''; // Clear the timer div
        question_text_element.innerText = 'Quiz Finished!'; // Display quiz finished message
        answers_ul_element.innerHTML = ''; // Clear the answers list

        // Display the final scores
        final_scores.forEach((user) => {
            const li = document.createElement('li');
            li.innerText = `${user.username}: ${user.score}`;
            answers_ul_element.appendChild(li);
        });
    }})
