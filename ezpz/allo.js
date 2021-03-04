const {spawn}=require('child_process');
const childPython=spawn('python',['compare1.py']);

childPython.stdout.on('data', (data) => {
   
 
    console.log(parseInt(data));
});

childPython.stderr.on('data',(data)=>{
    console.error('stderr: +(data)');
});