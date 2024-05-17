document.addEventListener('DOMContentLoaded', (event) => {
    const ws = new WebSocket('ws://localhost:8000/ws/quiz/');

    ws.onmessage = function (e) {
        const data = JSON.parse(e.data);
        const message = data.message;

        if (message.type === 'update_selection') {
            updateSelection(message.user_id, message.selection);
        } else if (message.type === 'new_question') {
            loadNewQuestion(message.question);
        }
    };

    document.querySelectorAll('.answer-option').forEach(option => {
        option.addEventListener('click', () => {
            const selection = option.dataset.value;
            ws.send(JSON.stringify({
                'message': {
                    'type': 'select_answer',
                    'selection': selection
                }
            }));
        });
    });

    function updateSelection(userId, selection) {
        // Update the UI to show the user's selection
    }

    function loadNewQuestion(question) {
        // Update the UI to show the new question and answers
    }
});
