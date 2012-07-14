var debug0;
var debug;
var debug2;
var debug3;
var courseTypeTable = {
  '30': '公选',
  '21': '专选',
  '11': '专必',
  '10': '公必'
};
var courseStatusTable = {
  '00': '不通过',
  '01': '待筛选',
  '03': '待审核',
  '04': '待确认',
  '05': '选课成功',
  '06': '已退课'
};
var examineTypeTable = {
  '01': '笔试',
  '02': '口试',
  '03': '考查',
  '04': '操作',
  '05': '其他'
};
var CampusTable = {
  '1': '南校区',
  '2': '北校区',
  '3': '猪海校区',
  '4': '中东'
};


$(document).ready(function(event) {
  $('.btn-group').click(function(event) {
    event.preventDefault();
  });

  $("#selecting-course-type").change(function() {
    if ($(this).val() == "30") {
      $("#selecting-course-campus").attr('disabled', false);
    }
    else {
      $("#selecting-course-campus").attr('disabled', true);
    }
  })

  $('.remove-class-btn').live('click', function(){
    var choice = confirm('确定退课？');
    var that = this;
    if (choice) {
      $.get('./remove_course', {'id': $(this).val()}, function(data) {
        eval('data = ' + data);
        $(that).replaceWith("<span>" + "退课状态:" + data.body.parameters.dataSave + "(请重新查询进行确认)" + "</span>");
      });
    }
  });

  $('.select-class-btn').live('click', function(){
    var choice = confirm('确定选课？');
    var that = this;
    if (choice) {
      $.get('./select_course', {'id': $(this).val(),
                                'year': $('#selecting-course-year').val(), 
                                'term': $('#selecting-course-term').val()}, function(data) {
        eval('data = ' + data);
        console.log(data);
        $(that).replaceWith("<span>" + "选课状态:" + data.body.parameters.dataSave + "(请查询选课结果进行确认)" + "</span>");
      });
    }
  });

  // get score results
  $('#score-query-btn').click(function(event) {
    event.preventDefault();
    $('#score-result').empty().append($('<img>').attr('src', './static/img/loading.gif'));

    var year = $('#score-year').val();

    // create table header
    var $tblHead = $('<thead>');
    $tblHead.append(
      $('<tr>').append($('<td>').text('课程名称'),
                       $('<td>').text('学期'),
                       $('<td>').text('学分'),
                       $('<td>').text('课程类别'),
                       $('<td>').text('成绩'),
                       $('<td>').text('绩点'),
                       $('<td>').text('教学班排名'))
    );

    // create table body
    var $tblBody = $('<tbody>');

    var $btnGroup = $('.btn-group')[0];
    $btnGroup = $($btnGroup).children();
    for (var termIdx = 0; termIdx < 3; termIdx++) {
      if ($($btnGroup[termIdx]).hasClass('active')) {
        // get score and fill in body
        $.get('./score', {'year': year, 'term': termIdx+1}, 
              function(data) {
                eval('data = ' + data);
                var score = data.body.dataStores.kccjStore.rowSet.primary;

                for (var i=0; i < score.length; i++) {
                  $tblBody.append(
                    $('<tr>').append($('<td>').text(score[i].kcmc),
                                     $('<td>').text(score[i].xq),
                                     $('<td>').text(score[i].xf),
                                     $('<td>').text(courseTypeTable[score[i].kclb]),
                                     $('<td>').text(score[i].zzcj),
                                     $('<td>').text(score[i].jd),
                                     $('<td>').text(score[i].jxbpm))
                  );
                };

                // combine head and body of the form
                var $tbl = $('<table>').attr({'class': 'table table-striped table-bordered table-condensed'})
                .append($tblHead, $tblBody);
                $('#score-result').empty().append($tbl);
              });
      }
    }
  });

  // bind event to btn select course
  $('#selecting-course-query-btn').click(function(event) {
    event.preventDefault();

    var year = $('#selecting-course-year').val();
    var term = $('#selecting-course-term').val();
    var type = $('#selecting-course-type').val();
    var campus = 0;
    if (type == "30") {
      campus = $('#selecting-course-campus').val();
    }

    // get course to be selected 
    $.get('./selecting_course', {'year': year, 'term': term, 'course_type': type, 'campus': campus}, 
          function(data) {
            eval('data=' + data);
            debug = data;

            var $tblHead = $('<thead>');
            $tblHead.append(
              $('<tr>').append($('<td>').text('课程名称'),
                               $('<td>').text('上课时间地点'),
                               $('<td>').text('任课老师'),
                               $('<td>').text('学分'),
                               $('<td>').text('课容量'),
                               $('<td>').text('待筛选人数'),
                               $('<td>').text('空位'),
                               $('<td>').text('开课单位'),
                               $('<td>').text('所在校区'),
                               $('<td>').text('选课'))
            );

            // create table body
            var $tblBody = $('<tbody>');
            var courses = data.body.dataStores.table1kxkcStore.rowSet.primary;

            for (var i=0; i < courses.length; i++) {
              $tblBody.append(
                $('<tr>').append($('<td>').text(courses[i].kcmc),
                                 $('<td>').text(courses[i].sksjdd),
                                 $('<td>').text(courses[i].zjjszc || ""),
                                 $('<td>').text(courses[i].xf),
                                 $('<td>').text(courses[i].xdrs),
                                 $('<td>').text(courses[i].xkrs),
                                 $('<td>').text(courses[i].syrs),
                                 $('<td>').text(courses[i].kkdwmc || ""),
                                 $('<td>').text(CampusTable[courses[i].skjsszxq]),
                                 $('<td>').html($('<button>').text('选课')
                                          .addClass('btn btn-success select-class-btn')
                                          .val(courses[i].jxbh)))
              );
            };
            // combine head and body of the form
            var $tbl = $('<table>').attr({'class': 'table table-striped table-bordered table-condensed'})
            .append($tblHead, $tblBody);
            $('#selecting-course-result').empty().append($tbl);
          });


  });

  // bind event to btn get course result
  $('#course-result-query-btn').click(function(event) {
    event.preventDefault();
    var year = $('#course-result-year').val();
    var term = $('#course-result-term').val();

    $.get('./course_result', {'year': year, 'term': term}, 
          function(data) {
            eval('data=' + data);
            debug = data;

            var $tblHead = $('<thead>');
            $tblHead.append(
              $('<tr>').append($('<td>').text('课程名称'),
                               $('<td>').text('课程类别'),
                               $('<td>').text('学分'),
                               $('<td>').text('选课状态'),
				                       $('<td>').text('考核方式'),
                               $('<td>').text('退课'))
            );

            // create table body
            var $tblBody = $('<tbody>');
            var courses = data.body.dataStores.xsxkjgStore.rowSet.primary;
            console.log(courses)

            for (var i=0; i < courses.length; i++) {
              $tblBody.append(
                $('<tr>').append($('<td>').text(courses[i].kcmc),
                                 $('<td>').text(courseTypeTable[courses[i].kclbm]),
                                 $('<td>').text(courses[i].xf),
                                 $('<td>').text(courseStatusTable[courses[i].xkcgbz]),
                                 $('<td>').text(examineTypeTable[courses[i].khfs] || ""),
                                 $('<td>').html($('<button>').text('退课')
                                                             .addClass('btn btn-danger remove-class-btn')
                                                             .val(courses[i].resource_id)))
              );
            };
            // combine head and body of the form
            var $tbl = $('<table>').attr({'class': 'table table-striped table-bordered table-condensed'})
            .append($tblHead, $tblBody);
            $('#course-result').empty().append($tbl);
          });
  });

  // bing event to btn get gpa and credit 
  $('#credit-gpa-query-btn').click(function(event) {
    event.preventDefault();
    // get tno and grade according to your sno
    $.get('./info', 
          function(data) {
            eval('data=' + data);
            debug0 = data;
            info = data.body.parameters.result.split(',');
            grade = info[1];
            tno = info[2];
            // get overall credit
            $.get('./overall_credit', {'grade': grade, 'tno': tno}, 
                  function(data) {
                    eval('data=' + data);
                    debug = data;

                    data = data.body.dataStores.zxzyxfStore.rowSet.primary;
                    var $tblHead = $('<thead>');
                    var $tblBody = $('<tbody>');
                    for (var i=0; i < data.length; i++) {
                      $tblBody.append(
                        $('<tr>').append($('<td>').text(data[i].oneColumn),
                                         $('<td>').text(data[i].twoColumn))
                      );
                    }
                    var $tbl = $('<table>').attr({'class': 'table table-striped table-bordered table-condensed'})
                    .append($tblHead, $tblBody);
                    $('#overall-credit-result').empty().append($tbl);
                  }
                 );
          }
         );

         // get obtained credit
         $.get('./obtained_credit',
               function(data) {
                 eval('data=' + data);
                 debug2 = data;

                 data = data.body.dataStores.allJdStore.rowSet.primary;
                 var $tblHead = $('<thead>');
                 var $tblBody = $('<tbody>');
                 for (var i=0; i < data.length; i++) {
                   $tblBody.append(
                     $('<tr>').append($('<td>').text(data[i].oneColumn),
                                      $('<td>').text(data[i].twoColumn))
                   );
                 }
                 var $tbl = $('<table>').attr({'class': 'table table-striped table-bordered table-condensed'})
                 .append($tblHead, $tblBody);
                 $('#obtained-credit-result').empty().append($tbl);
               }
              );

              // get gpa
              $.get('./gpa',
                    function(data) {
                      eval('data=' + data);
                      debug3 = data;

                      data = data.body.dataStores.allJdStore.rowSet.primary;
                      var $tblHead = $('<thead>');
                      var $tblBody = $('<tbody>');
                      for (var i=0; i < data.length; i++) {
                        $tblBody.append(
                          $('<tr>').append($('<td>').text(data[i].oneColumn),
                                           $('<td>').text(data[i].twoColumn))
                        );
                      }
                      var $tbl = $('<table>').attr({'class': 'table table-striped table-bordered table-condensed'})
                      .append($tblHead, $tblBody);
                      $('#gpa-result').empty().append($tbl);
                    }
                   );

  });
});
