import webbrowser
import subprocess
import os


test_file = 'test.html'

f = open(test_file, 'w')

message = """
<!DOCTYPE html>
<html>
<title>W3.CSS</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
.mySlides {display:none;}
body { margin:0; }
</style>
<body>
<div class="images" style="width:100%, height:100%">
  <img class="mySlides" src="https://ifsstech.files.wordpress.com/2008/10/169.jpg" style="width:100%">
  <img class="mySlides" src="https://designshack.net/wp-content/uploads/16-9.jpg" style="width:100%">
  <img class="mySlides" src="https://upload.wikimedia.org/wikipedia/commons/7/7c/Aspect_ratio_16_9_example.jpg" style="width:100%">
</div>

<script>
var myIndex = 0;
carousel();

function carousel() {
    var i;
    var x = document.getElementsByClassName("mySlides");
    for (i = 0; i < x.length; i++) {
       x[i].style.display = "none";  
    }
    myIndex++;
    if (myIndex > x.length) {myIndex = 1}    
    x[myIndex-1].style.display = "block";  
    setTimeout(carousel, 200); // Change image every 2 seconds
}
</script>

</body>
</html>
"""

f.write(message)
f.close()

fscreen = "./Fullscreen"
first = False
if not os.path.isfile(fscreen):
    first = True
    os.environ["DISPLAY"] = ":0"

webbrowser.register('midori', None, webbrowser.BackgroundBrowser('/usr/bin/midori'))
browser = webbrowser.get('midori')
browser.open(test_file)
if first:
    subprocess.call('xte "key F11" -x:0', shell=True)
    open(fscreen,'a').close()

