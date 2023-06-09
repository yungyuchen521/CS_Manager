
// JavaScript Document
$(document).ready(function(){//都要包在這個裡面


    //匯出成 PDF 檔案的功能
    //點擊匯出按鈕後，發送 request 到後端的 export_to_pdf，export_to_pdf 回傳 response 到前端生成下載點
    const exportBtn = document.getElementById('export-pdf-btn');
    exportBtn.addEventListener('click', () => {
        // 发送请求到后端视图函数
        fetch('/export-to-pdf/')
            .then(response => response.blob())
            .then(blob => {
                // 创建下载链接
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;

                // 取得當天日其
                var today = new Date();
                var year = today.getFullYear();
                var month = today.getMonth() + 1;
                var day = today.getDate();
                var formattedDate = year + '-' + (month < 10 ? '0' + month : month) + '-' + (day < 10 ? '0' + day : day);

                console.log("formattedDate", formattedDate);  // 輸出：YYYY-MM-DD 格式的當天日期

                a.download = formattedDate + '.pdf';
                a.click();
                window.URL.revokeObjectURL(url);
            });
    });
});