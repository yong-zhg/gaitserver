var CONSTANT = {
            DATA_TABLES : {
                DEFAULT_OPTION :{
                language: {
                    "sProcessing": "处理中...",
//                    "sLengthMenu": "显示 _MENU_ 项结果",
                    "sZeroRecords": "没有匹配结果",
//                    "sInfo": "显示第 _START_ 至 _END_ 项结果，共 _TOTAL_ 项",
//                    "sInfoEmpty": "显示第 0 至 0 项结果，共 0 项",
//                    "sInfoFiltered": "(由 _MAX_ 项结果过滤)",
                    "sInfoPostFix": "",
                    "sSearch": "搜索:",
                    "sUrl": "",
                    "sEmptyTable": "表中数据为空",
                    "sLoadingRecords": "载入中...",
                    "sInfoThousands": ",",
                    "oPaginate": {
                        "sFirst": "首页",
                        "sPrevious": "上页",
                        "sNext": "下页",
                        "sLast": "末页"
                    },
                    "oAria": {
                        "sSortAscending": ": 以升序排列此列",
                        "sSortDescending": ": 以降序排列此列"
                    }
                },
                searching: false,
                ordering:  false,
                serverSide: true,
                //retrieve:true,
                destroy:true,
                "aoColumns": [
                    {"mDataProp":"start_time"},
                    {"mDataProp":"end_time"},
                    {"mDataProp":"steps"}
                ],
                "columnDefs" : [{
                    "render" : function(data, type, row) {
                        //console.log(data);
                        if ( type === 'display' || type === 'filter' ) {
                            var d = new Date(data);
                            //console.log(d);
                            var time = d.getFullYear()+"年"+(d.getMonth()+1)+"月"+d.getDate()+"日"+d.getHours()+":"+d.getMinutes()+":"+d.getSeconds();
                            return time;
                        }
                    },
                "targets" : [0,1]
                }],
            }
        }
    };