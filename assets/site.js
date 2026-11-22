(()=>{
  const loads=new Map();
  const source=url=>{if(!loads.has(url))loads.set(url,fetch(url).then(response=>{if(!response.ok)throw Error('无法读取文件');return response.text();}).catch(error=>{loads.delete(url);throw error;}));return loads.get(url);};
  document.querySelectorAll('[data-copy-code]').forEach(button=>button.addEventListener('click',async()=>{
    const label=button.textContent;button.disabled=true;const status=document.getElementById('copy-status');
    try{
      const text=await source(button.dataset.copyCode);
      if(navigator.clipboard&&window.isSecureContext)await navigator.clipboard.writeText(text);
      else{const input=document.createElement('textarea');input.value=text;input.style.cssText='position:fixed;left:-9999px';document.body.append(input);input.select();const copied=document.execCommand('copy');input.remove();if(!copied)throw Error('请打开 TXT 文件全选复制');}
      button.textContent='已复制代码';if(status)status.textContent='代码已复制，打开 Scriptable 新建脚本并粘贴。';
    }catch(error){if(status)status.textContent='暂时无法复制，请打开 TXT 文件后全选复制。';}
    finally{button.disabled=false;setTimeout(()=>button.textContent=label,2500);}
  }));
  document.querySelectorAll('details[data-source]').forEach(details=>details.addEventListener('toggle',async()=>{if(!details.open||details.dataset.loaded)return;const code=details.querySelector('code');try{code.textContent=await source(details.dataset.source);details.dataset.loaded='true';}catch(error){code.textContent='读取失败，请使用上方下载按钮重试。';}}));
})();
