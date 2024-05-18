document.addEventListener('DOMContentLoaded', (event) => {
    //    const ws = new WebSocket('ws://localhost:8000/ws/quiz/');
    const quizSocket = new WebSocket('ws://' + window.location.host + '/ws/quiz/');

    quizSocket.onmessage = function (e) {
        const data = JSON.parse(e.data);
        //ahhhS
        if (data.type === 'game_state') {
            const gameState = data.game_state
            document.getElementById('current-question').innerText = gameState.current_question;
            document.getElementById('quiz-type').innerText = gameState.quizType;

            document.getElementById('question-text').innerText = gameState.question;

           // answers = gameState.answers;
            const answersList = document.getElementById('answers-list');
            answersList.innerHTML = '';
            const li = document.createElement('li');
            li.innerText = "I have no idea lol";
            answersList.appendChild(li);
            //answers.forEach((answer, index) => {
            //    const li = document.createElement('li');
            //    li.innerText = answer.text;
            //    li.addEventListener('click', function () {
            //        // Remove 'selected' class from all list items
            //        const allAnswers = answersList.querySelectorAll('li');
            //        allAnswers.forEach(item => item.classList.remove('toggled'));
            //        allAnswers.forEach(item => item.removeAttribute("id", "correct"));

            //        // Add 'selected' class to the clicked item
            //        this.classList.add('toggled');

            //        if (answer.is_correct == true) {
            //            this.setAttribute("id", "correct");
            //        }

            //        // Send the selected answer to the server
            //        quizSocket.send(JSON.stringify({
            //            'type': 'answer_selected',
            //            'answer_index': this.dataset.index,
            //        }));
            //    });
            //    answersList.appendChild(li);
            //});
        }else if (data.type === 'user_list') {
            // Handle user list update
            const userList = document.getElementById('user_list');
            userList.innerHTML = '';  // Clear the current list
            data.users.forEach(username => {
                const li = document.createElement('li');
                li.innerText = username + ": ___";
                li.setAttribute("id", `username-${username}`)
                userList.appendChild(li);
            });
        }

        //should activate when a user makes selection
        if (data.type === 'user_selection') {
            username = data.username;

            // Update UI to indicate user selection
            const usernameElement = document.getElementById(`username-${username}`);
            if (usernameElement) {
                usernameElement.classList.add('chosen');
            }
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

