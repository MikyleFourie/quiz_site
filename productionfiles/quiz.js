document.addEventListener('DOMContentLoaded', (event) => {
    //    const ws = new WebSocket('ws://localhost:8000/ws/quiz/');
    const quizSocket = new WebSocket('ws://' + window.location.host + '/ws/quiz/');

    quizSocket.onmessage = function (e) {
        const data1 = JSON.parse(e.data);
        if (data1.type === 'game_state') {
            const gameState = data1.game_state;
            document.getElementById('current-question').innerText = gameState.current_question;
            // Update other parts of the DOM based on the game state if needed
        }

        const data2 = JSON.parse(e.data);
        if (data2.type === 'initial_data') {
            const question = data2.data.question_text;
            const answers = data2.data.answers;
            document.getElementById('question-text').innerText = question;
            const answersList = document.getElementById('answers-list');
            answersList.innerHTML = '';
            answers.forEach((answer, index) => {
                const li = document.createElement('li');
                li.innerText = answer.text;
                li.addEventListener('click', function () {
                    // Remove 'selected' class from all list items
                    const allAnswers = answersList.querySelectorAll('li');
                    allAnswers.forEach(item => item.classList.remove('toggled'));

                    // Add 'selected' class to the clicked item
                    this.classList.add('toggled');

                    // Send the selected answer to the server (optional)
                    quizSocket.send(JSON.stringify({
                        'type': 'answer_selected',
                        'answer_index': this.dataset.index
                    }));
                });
                answersList.appendChild(li);
            });
        }

        if (data2.type === 'user_list') {
            // Handle user list update
            const userList = document.getElementById('user_list');
            userList.innerHTML = '';  // Clear the current list
            data2.users.forEach(username => {
                const li = document.createElement('li');
                li.innerText = username;
                userList.appendChild(li);
            });
        }
    };
    //ws.onmessage = function (e) {
    //    const data = JSON.parse(e.data);
    //    const message = data.message;

    //    if (message.type === 'update_selection') {
    //        updateSelection(message.user_id, message.selection);
    //    } else if (message.type === 'new_question') {
    //        loadNewQuestion(message.question);
    //    }
    //};

    //document.querySelectorAll('.answer-option').forEach(option => {
    //    option.addEventListener('click', () => {
    //        const selection = option.dataset.value;
    //        ws.send(JSON.stringify({
    //            'message': {
    //                'type': 'select_answer',
    //                'selection': selection
    //            }
    //        }));
    //    });
    //});

    //function updateSelection(userId, selection) {
    //    // Update the UI to show the user's selection
    //}

    //function loadNewQuestion(question) {
    //    // Update the UI to show the new question and answers
    //}
});

