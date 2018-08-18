$("#querytime").click(function(){
    var s_time = $('#dtp_input1').val().replace(/-/g,' ');
    var e_time = $('#dtp_input2').val().replace(/-/g,' ');
    start_time = Date.parse(s_time);
    end_time = Date.parse(e_time);
    console.log(start_time);
    console.log(end_time);
    console.log(s_time);
    console.log(e_time);
    if (!s_time || !e_time){
        alert('请选择时间');
    }
    else{
        postJSON('/data/step/pages/count', {
            token: t_token,
            filter: {
                start_time: start_time,
                end_time: end_time,
            },
            page: {
                page_size: 20
            }
        },  function(result) {
            if ( !result || !result.successful ) {
                alert('获取数据失败');
            }
            else {
                total_c = result.data.total_count;
                console.log(result.data.total_count);
                console.log(total_c);
                get_table(total_c);
                return;
            }
        });
    }
})