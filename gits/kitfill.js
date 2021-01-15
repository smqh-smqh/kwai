document.getElementsByClassName("ivu-btn ivu-btn-primary")[2].setAttribute("onclick", "showres()");
var wrap=document.createElement("textarea");
wrap.setAttribute("placeholder","请填入curl格式");
wrap.setAttribute("class","ivu-input");
wrap.setAttribute("style","overflow-y:visible; ");
wrap.setAttribute("rows","5");
var first=document.body.firstChild;
var div = document.createElement("div");
var br = document.createElement("br");
div.appendChild(wrap);
div.appendChild(br);

var button1 = document.createElement("input");
button1.setAttribute("type", "button");
button1.setAttribute("value", "提交");
button1.setAttribute("id", "bt1");
button1.setAttribute("onclick", "split(this.id)");
button1.setAttribute("class", "ivu-btn ivu-btn-primary");
button1.setAttribute("style", "margin:10px;");

var button2 = document.createElement("input");
button2.setAttribute("type", "button");
button2.setAttribute("value", "清除");
button2.setAttribute("id", "bt2");
button2.setAttribute("onclick", "split(this.id)");
button2.setAttribute("class", "ivu-btn ivu-btn-primary");
button2.setAttribute("style", "margin:10px;");

var bt2=document.body.insertBefore(button2,first);
var bt1=document.body.insertBefore(button1, button2);
var wraphtml =document.body.insertBefore(div, button1);


function split(id){
	if(id == 'bt2'){
	 	wrap.value = '';
		return;
	}
	// getInputByPlaceHolderJS("curl -H ... --data ...").value=wrap.value;
	let str = wrap.value.replace(/\'/g,"").split(" -H ");
	if(!str[0].startsWith("curl")){
		alert('需要填入curl格式哦');
		return;
	}

	let arrUrl="";
	if(str[str.length-1].search(" --compressed ")>0){
		arrUrl=str[str.length-1].split(" --compressed ")[1];
		str[str.length-1]=str[str.length-1].split(" --compressed ")[0];
	}else{
            let s = str[str.length-1].indexOf("http");
            arrUrl = str[str.length-1].substring(s);
            str[str.length-1] = str[str.length-1].substring(0,s);
        
	}
	var event = new Event('input');
	arrUrl=arrUrl.split("://");
	let start = arrUrl[1].indexOf("/");
	let host = arrUrl[1].substring(0,start);
　　 let urls = arrUrl[1].substring(start);
　　 if(urls.indexOf("?") != -1){
　　　　　　var url = urls.split("?")[0];
		  let query = urls.split("?")[1];
		  console.log(query);
		  let a = document.getElementsByClassName("ivu-input")[5];
		  a.value=query;
		  a.dispatchEvent(event);
　　 }
	console.log(host);
	let b=getInputByPlaceHolderJS("请输入host");
	b.value=host;
	b.dispatchEvent(event);
	console.log(url);
	let c=getInputByPlaceHolderJS("请输入接口路径");
	c.value=url;
	c.dispatchEvent(event);

	let radios = document.getElementsByClassName("ivu-radio-input");
	if(arrUrl[0] == 'https'){
		console.log('https');
		radios[6].click();
	}else{
		console.log('http');
		radios[5].click();
	}

	let last = str[str.length-1];
	if(last.search("--data")>0){
		console.log('POST')	;	
		radios[3].click();
		let begin = last.indexOf("--data");
        str[str.length-1] = last.substring(0,begin);
		let reg = /\"(.+?)\"/;
		let string = "'"+ str[str.length-1]+"'";
    	let data = reg.exec(string);
		if(data!=null){
			let d=getInputByPlaceHolderJS("key1=value1&key2=value3...");
			d.value=data[1];
			d.dispatchEvent(event);
			console.log('form-data: '+data[1]);
		}		
	}else{
		console.log('GET');
		radios[4].click();
	}
	
	let n=4; let aa=""; let bb="";
	for(let para of str){
        if(para.startsWith(":")) para=para.substring(1);
		if(para.indexOf(":") != -1){
			document.getElementsByClassName("ivu-btn ivu-btn-dashed")[0].click();
			sleep(1000).then(()=>{
                let pas=para.split(':');
                if(aa!=pas[0]){
                    aa=pas[0]; bb=pas[1];
                    if(aa=="Cookie"||aa=="cookie") bb="${cookie}";
                    console.log(aa+"  "+bb);
                    let e=document.getElementsByClassName("ivu-input ivu-input-default")[n++];
                    e.value=aa;
                    e.dispatchEvent(event);
                    let f=document.getElementsByClassName("ivu-input ivu-input-default")[n++];
                    f.value=bb;
                    f.dispatchEvent(event);
                }
			});
		}		
	}
	alert("解析成功");
}

function sleep(ms) {
	return new Promise(resolve => setTimeout(resolve, ms));
}


function getInputByPlaceHolderJS(placeholder) {
    var curPlaceholder;
    for (var i = 0; i < document.getElementsByTagName("input").length
; i++) {
        curPlaceholder = document.getElementsByTagName("input")[i].placeholder;
        if (curPlaceholder && curPlaceholder.indexOf(placeholder) != -1) {
            return document.getElementsByTagName("input")[i];
        }
    }
    for (var i = 0; i < document.getElementsByTagName("textarea").length; i++) {
        curPlaceholder = document.getElementsByTagName("textarea")[i].placeholder;
        if (curPlaceholder && curPlaceholder.indexOf(placeholder) != -1) {
            return document.getElementsByTagName("textarea")[i];
        }
    }
}


function insertAfter( newElement, targetElement ){ // newElement是要追加的元素 targetElement 是指定元素的位置 
    var parent = targetElement.parentNode; // 找到指定元素的父节点 
    if( parent.lastChild == targetElement ){ // 判断指定元素的是否是节点中的最后一个位置 如果是的话就直接使用appendChild方法 
        parent.appendChild( newElement, targetElement ); 
    }else{ 
        parent.insertBefore( newElement, targetElement.nextSibling ); 
    }; 
}; 

function showres(){	
	let i=20;
	let flag=false;
	while(i>0){
		i--;
		sleep(500).then(()=>{
			if(document.getElementById("api_test_result")!=null){
				// let text=document.getElementById("api_test_result").innerText;
				// text = text.replace(/\-/g,"");
				// jsonres.value=JSON.stringify(JSON.parse(text), null, "\t");
				flag=true;
				document.getElementsByClassName("ivu-btn ivu-btn-error ivu-btn-large")[1].click();
				var last=document.body.lastChild;
				var code = document.getElementById("api_test_result");
				// var newcode = code.cloneNode(true);
				insertAfter(code,last);
			}
		});								
		if(flag) break;
	}	
}