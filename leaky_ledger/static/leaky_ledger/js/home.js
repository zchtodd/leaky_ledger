function updateElementText(element, textArray) {
    var i = 0;
    setInterval(function() {
        $(element).fadeOut('slow', function() {
            $(this).text(textArray[i]);
            $(this).fadeIn('slow');
        });
        i++;
        if (i >= textArray.length) {
            i = 0;
        }
    }, 10000);
}

var textArray = [
  "With Leaky Ledger, the security of my account is something I can always be uncertain about. One day, I found out that I'd bought a goat farm in Mongolia - I've always wanted to be an entrepreneur, I just didn't know it yet!",
  "Thanks to their remarkable banking alerts, I found out I was holidaying in Bora Bora. I have no memory of this trip, but the transactions don't lie! I even had a yacht rental on the bill – who knew I was living such a lavish lifestyle?",
  "Their customer service? Exemplary. It only took six calls, two emails, and a strongly worded letter to get their attention. And then, with a simple 'oops, our bad', all was set right. I could feel the care and dedication.",
  "I must say, being with Leaky Ledger has been like playing the lottery - I never know what's going to show up on my bank statement next. It's like a surprise party that never ends."
];

var element = document.getElementById("testimonial-text");
updateElementText(element, textArray);
