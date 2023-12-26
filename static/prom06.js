/**
* PROM06 Chatbot Creator
* by
* Glenn Tam
*/


// Init state variables.
var state = 0;
var rawText = '';


/**
* A helper function to present the bot's output into HTML.
* The parent bot and the child bot are styled differently.
* @param {string} phrase - The bot's response
*/
function botOutput(phrase) {
  if (state < 2) {
    botNum = 'firstBot';
    botName = 'CHATBOT';
  } else {
    botNum = 'secondBot';
    botName = 'MY CHATBOT';
  }
  htmlWrapper = '<p class="' + botNum + '"><span>' + botName + ': ' + phrase + '</span></p>';
  $("#conversationContainer").append(htmlWrapper);
}


/**
* A helper function to present the user's input as HTML.
* @param {string} phrase - The user's input
*/
function userInput(phrase) {
  htmlWrapper = '<p class="userText"><span>' + phrase + '</span></p>';
  $("#conversationContainer").append(htmlWrapper);
}


// Output instructions
botOutput("Hi, I can help you create a new chatbot if you give me some training data.");
botOutput("Type in some information you want your new AI to know (you can also copy and paste a whole body of text).");


/**
* Send the user's input to the server and print the bot's response
* @returns {Null}
*/
function getBotResponse() {
  // check for empty input
  $("#submitBtn").prop("disabled", true);
  rawText = $("#textBox").val();
  checkEmpty: if (/[a-z]/i.test(rawText) === false) {
    $("#textBox").val('');
    if (state == 0) {
      $("#textBox").prop('placeholder', 'Please enter some training text first');
    } else if (state == 1) {
      $("#textBox").prop('placeholder', "If you're finished adding training data, please click the red button below to begin training your new chatbot!");
    } else if (state == 2) {
      break checkEmpty;
    } else if (state == 3) {
      $("#textBox").prop('placeholder', "Try to ask your new chatbot something related");
    }
    $("#submitBtn").prop("disabled", false);
    return
  }
  // process input
  userInput(rawText);
  $("#textBox").val('');
  var callServer = state + rawText;
  $.get("/bot", { msg: callServer }).done(function(data) {
    if (state < 2) {
      var botHtml = '<p class="firstBot"><span>CHATBOT: ' + data + '</span></p>';
      $("#createBtn").prop("disabled", false);
      $("#createBtn").prop('value', 'Finish conversational training. Click to create AI.');
      $("#textBox").val('');
      $("#textBox").prop('placeholder', 'Enter more training data, or press the red button to begin training your AI');
      state = 1;
    } else if (state == 2) {
      $("#createBtn").prop("disabled", true);
      $("#createBtn").prop('value', 'Ask your chatbot something related');
      $("#textBox").val('');
      $("#textBox").prop('placeholder', 'Talk to your trained chatbot now');
      state = 3;
    } else if (state == 3) {
      $("#createBtn").prop("disabled", false);
      $("#createBtn").prop('value', 'CLICK HERE TO FINISH');
      $("#createBtn").click(function(){
  	$("#feedback").css("display", "block");
      })
      $("#textBox").prop('placeholder', 'Continue talking to your new chatbot OR click the RED BUTTON when finished');
      state = 4;
    }
    // show bot output
    botOutput(data);
    document.getElementById("uiContainer").scrollIntoView({block: 'start', behavior: 'smooth'});
    $("#submitBtn").prop("disabled", false);
  });
}


/**
* Create a new chatbot based on the user's training data
* @returns {Null}
*/
function createNewChatbot() {
  $("#textBox").val('');
  $("#textBox").prop('placeholder', 'Talk to your trained chatbot now');
  botOutput("One moment please. Creating your new AI chatbot now...");
  state = 2;
  getBotResponse();
}


/**
* Show consent form on page load and get consent to begin
*/
$(document).ready(function(){
  $("#consent").fadeIn("slow");
});
function begin() {
  $("#consent").fadeOut("slow", function() {
  $("#main").fadeIn("slow");
 });
}
