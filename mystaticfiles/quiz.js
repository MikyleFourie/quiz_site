
document.addEventListener('DOMContentLoaded', (event) => {

    // Extract the quiz title from the current URL
    const pathParts = window.location.pathname.split('/');
    const quizTitle = pathParts[pathParts.length - 2]; // Assuming URL ends with quiz/<title>/

    // Get the protocol of the current window
    const protocol = window.location.protocol === 'https:' ? 'wss://' : 'ws://';

    // Construct the WebSocket URL
    //const quizSocket = new WebSocket('ws://' + window.location.host + '/ws/quiz/'+ quizTitle + '/');
    //const quizSocket = new WebSocket(  'wss://' + window.location.host + '/wss/quiz/' + quizTitle + '/');
    //has to match with:                wss://ppg-quiz-site-265ccf6f2c38.herokuapp.com/wss/quiz/Art/
    const quizSocket = new WebSocket(protocol + window.location.host + '/ws/quiz/' + quizTitle + '/');


    //Get all HTML containers we need to manipulate
    const current_question_num_element = document.getElementById('current-question');
    const current_quiz_type_element = document.getElementById('quiz-type');
    const question_text_element = document.getElementById('question-text');
    const answers_ul_element = document.getElementById('answers-list');
    const user_ul_element = document.getElementById('user_list');
    const numOfUsers_element = document.getElementById('numOfUsers');

    //document.getElementById('quizForm').onsubmit = function (e) {
    //    console.log("form.onSubmit ran!");
    //    e.preventDefault();
    //    const formData = new FormData(this);
    //    const formObj = {};
    //    formData.forEach((value, key) => { formObj[key] = value; });
    //    quizSocket.send(JSON.stringify({
    //        'type': 'form_message',
    //        'message': formObj,
    //    }));
    //};

    //document.querySelectorAll('#quizForm input[type="radio"]').forEach(input => {

    //    input.addEventListener('change', () => {
    //        submitForm();
    //        console.log("it radioed!", input.value);
    //    });
    //});

    //function submitForm() {
    //    document.getElementById("quizForm").submit();
    //    console.log("it submitted!");
    //}

    


    quizSocket.onmessage = function (e) {
        const data = JSON.parse(e.data);

        //if (data.type == 'check') {
        //    const message = data['message'];
        //    console.log(message)

        //    document.getElementById('trbl').innerText = message;
        //}

        
        
        if (data.type === 'game_state') {
            const gameState = data.game_state
            current_question_num_element.innerText = gameState.current_question + 1;
            current_quiz_type_element.innerText = gameState.quizType;
            question_text_element.innerText = gameState.question;
            numOfUsers_element.innerText = gameState.numOfUsers;

            answers = gameState.answers;
            answers_ul_element.innerHTML = '';
            answers.forEach((answer, index) => {
                const li = document.createElement('li');
                li.innerText = answer.text;
                li.classList.add('unselected')

                //li.addEventListener('click', optionHandler);
                li.addEventListener('click', function clickHandler() {
                    if (this.classList.contains('unselected')) {
                        console.log("answer with ID:", answer.id);
                        console.log("--------");
                        const selectedOption = this; 

                        answers_ul_element.querySelectorAll('li').forEach(item => {
                            item.classList.remove('unselected');
                        });

                        // Add 'toggled' class to the clicked item
                        this.classList.add('toggled');

                        // Send the selected answer to the server
                        quizSocket.send(JSON.stringify({
                            'type': 'answer_selected',
                            'answer_id': answer.id,
                        }));
                    }                                 
                });
                answers_ul_element.appendChild(li);
            });
            //addAnswerListeners();
        }

        if (data.type === 'question_ids') {
            console.log("ping");
            qIds = data.question_ids;

            qIds.forEach((qId, index) => {
                const li = document.createElement('li');
                li.innerText = qId;
                answers_ul_element.appendChild(li);
            });

        }
        
        if (data.type === 'user_list') {
            ////Recieves 'user-list' broadcast. Handle user list update
            userList = data.user_list; //Gets user_list from broadcast
            user_ul_element.innerHTML = '';  // Clear the current list

            data.users.forEach(user => {
                const li = document.createElement('li');
                li.setAttribute("id", `username-${user.username}`);
                li.innerText = `${user.username}: ${user.score}`;
                user_ul_element.appendChild(li);
                console.log(`Name:${user.username} Score:${user.score}`);
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

        if (data.type === 'score_update') {
            username = data.username;

            const usernameElement = document.getElementById(`username-${username}`);
            if (usernameElement) {
                usernameElement.classList.remove('chosen');
            }
        }
        

        



    };


    

});

