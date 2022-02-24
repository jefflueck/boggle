let score = 0;

let words = new Set();

let time = 60;
$('#timer').html(time);

$('form').on('submit', handleSubmit);

async function handleSubmit(e) {
  e.preventDefault();

  let word = $('input').val();

  if (!word) return;

  const res = await axios.get('/word-compare', { params: { word: word } });

  let response = res.data.response;

  $('#response').html(response);

  $('form').trigger('reset');

  if (response === 'ok') {
    if (words.has(word)) {
      return;
    }
    words.add(word);
    score += word.length;
    $('#score').html(`Score: ${score}`);
  }
}

let countDown = setInterval(function () {
  time--;
  $('#timer').html(time);
  stopTimer();
}, 1000);

function stopTimer() {
  if (time < 1) {
    clearInterval(countDown);
    $('form').hide();
    $('.container').append($('<span>').html('Game Over'));
    endGame();
  }
}

async function endGame() {
  await axios.post('/end-game', { score: score });
}
