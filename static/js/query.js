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
  '01': '选课成功',
}

$(document).ready(function(event) {
  $('.btn-group').click(function(event) {
    event.preventDefault();
  });

  $('.add-class-btn').click(function(){
    alert('add!');
  });

  $('.remove-class-btn').live('click', function(){
    $.get('./remove_course', {'id': $(this).val()});
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
                       $('<td>').text('总评成绩'),
                       $('<td>').text('最终成绩'),
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
                                     $('<td>').text(score[i].zpcj),
                                     $('<td>').text(score[i].zzcj),
                                     $('<td>').text(score[i].jd),
                                     $('<td>').text(score[i].jxbpm))
                  );
                };
              });
      }
    }
    // combine head and body of the form
    var $tbl = $('<table>').attr({'class': 'table table-striped table-bordered table-condensed'})
    .append($tblHead, $tblBody);
    $('#score-result').empty().append($tbl);
  });

  // bind event to btn select course
  $('#select-course-query-btn').click(function(event) {
    event.preventDefault();
    var courseType = $('#select-course-type').val(); 

    // get course to be selected 
    $.get('./selecting_course', {'year': '2011-2012', 'term': 2, 'course_type': courseType}, 
          function(data) {
            eval('data=' + data);
            debug = data;

            var $tblHead = $('<thead>');
            $tblHead.append(
              $('<tr>').append($('<td>').text('操作'),
                               $('<td>').text('课程名称'),
                               $('<td>').text('上课时间地点'),
                               $('<td>').text('任课老师'),
                               $('<td>').text('学分'),
                               $('<td>').text('课容量'),
                               $('<td>').text('待筛选人数'),
                               $('<td>').text('空位'))
            );

            // create table body
            var $tblBody = $('<tbody>');
            var courses = data.body.dataStores.table1kxkcStore.rowSet.primary;

            for (var i=0; i < courses.length; i++) {
              $tblBody.append(
                $('<tr>').append($('<td>').html($('<button>').addClass('add-class-btn').text('选课')),
                                 $('<td>').text(courses[i].kcmc),
                                 $('<td>').text(courses[i].sksjdd),
                                 $('<td>').text(courses[i].zjjszc),
                                 $('<td>').text(courses[i].xf),
                                 $('<td>').text(courses[i].xdrs),
                                 $('<td>').text(courses[i].syrs),
                                 $('<td>').text(courses[i].syrs))
              );
            };
            // combine head and body of the form
            var $tbl = $('<table>').attr({'class': 'table table-striped table-bordered table-condensed'})
            .append($tblHead, $tblBody);
            $('#selecting-course-result').empty().append($tbl);
          });

          // get course have been selected 
          $.get('./selected_course', {'year': '2011-2012', 'term': 2, 'course_type': courseType}, 
                function(data) {
                  eval('data=' + data);
                  debug = data;

                  var $tblHead = $('<thead>');
                  $tblHead.append(
                    $('<tr>').append($('<td>').text('操作'),
                                     $('<td>').text('课程名称'),
                                     $('<td>').text('上课时间地点'),
                                     $('<td>').text('任课老师'),
                                     $('<td>').text('学分'),
                                     $('<td>').text('课容量'),
                                     $('<td>').text('待筛选人数'),
                                     $('<td>').text('空位'))
                  );

                  // create table body
                  var $tblBody = $('<tbody>');
                  var courses = data.body.dataStores.table1yxkcStore.rowSet.primary;

                  for (var i=0; i < courses.length; i++) {
                    $tblBody.append(
                      $('<tr>').append($('<td>').html($('<button>').addClass('remove-class-btn').text('退选').val(courses[i].resourceID)),
                                       $('<td>').text(courses[i].kcmc),
                                       $('<td>').text(courses[i].sksjjd),
                                       $('<td>').text(courses[i].zjjszc),
                                       $('<td>').text(courses[i].xf),
                                       $('<td>').text(courses[i].xdrs),
                                       $('<td>').text(courses[i].syrs),
                                       $('<td>').text(courses[i].syrs))
                    );
                  };
                  // combine head and body of the form
                  var $tbl = $('<table>').attr({'class': 'table table-striped table-bordered table-condensed'})
                  .append($tblHead, $tblBody);
                  $('#selected-course-result').empty().append($tbl);
                });
  });

  // bing event to btn get course result
  $('#course-result-query-btn').click(function(event) {
    event.preventDefault();
    $.get('./course_result', {'year': '2011-2012', 'term': 2}, 
          function(data) {
            eval('data=' + data);
            debug = data;

            var $tblHead = $('<thead>');
            $tblHead.append(
              $('<tr>').append($('<td>').text('课程名称'),
                               $('<td>').text('课程类别'),
                               $('<td>').text('学分'),
                               $('<td>').text('选课状态'))
            );

            // create table body
            var $tblBody = $('<tbody>');
            var courses = data.body.dataStores.xsxkjgStore.rowSet.primary;

            for (var i=0; i < courses.length; i++) {
              $tblBody.append(
                $('<tr>').append($('<td>').text(courses[i].kcmc),
                                 $('<td>').text(courseTypeTable[courses[i].kclbm]),
                                 $('<td>').text(courses[i].xf),
                                 $('<td>').text(courseStatusTable[courses[i].pylbm]))
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
    $.ajaxSetup({async:false});
    // get tno and grade according to your sno
    var info;
    $.get('./info', 
          function(data) {
            eval('data=' + data);
            debug = data;
            info = data.body.parameters.result.split(',');
          }
         );
    grade = info[1];
    tno = info[2];

    var overallCredit, obtainedCredit, gpa;
    // get overall credit
    $.get('./overall_credit', {'grade': grade, 'tno': tno}, 
          function(data) {
            eval('data=' + data);
            debug = data;

            overallCredit = data.body.dataStores.zxzyxfStore.rowSet.primary;
          }
         );

    // get obtained credit
    $.get('./obtained_credit',
          function(data) {
            eval('data=' + data);
            debug2 = data;

            obtainedCredit = data.body.dataStores.allJdStore.rowSet.primary;
          }
         );

    // get gpa
    $.get('./gpa',
          function(data) {
            eval('data=' + data);
            debug3 = data;

            gpa = data.body.dataStores.allJdStore.rowSet.primary;
          }
         );

    $.ajaxSetup({async:true});

    var $tblBody = $('<tbody>');
            for (var i=0; i < 5; i++) {
              $tblBody.append(
                $('<tr>').append($('<td>').text(overallCredit[i].oneColumn.substr(0, overallCredit[i].oneColumn.length-2)),
                                 $('<td>').text(typeof(overallCredit[i]) == 'undefined' ? 0 : overallCredit[i].twoColumn),
                                 $('<td>').text(typeof(obtainedCredit[i]) == 'undefined' ? 0 : obtainedCredit[i].twoColumn),
                                 $('<td>').text(typeof(gpa[i]) == 'undefined' ? 0 : gpa[i].twoColumn))
              );
            };
    var $tblHead = $('<thead>');
    $tblHead.append(
      $('<tr>').append($('<td>').text('课程类别'),
                       $('<td>').text('总学分'),
                       $('<td>').text('已修学分'),
                       $('<td>').text('绩点'))
    );
    var $tbl = $('<table>').attr({'class': 'table table-striped table-bordered table-condensed'})
    .append($tblHead, $tblBody);
    $('#credit-gpa-result').empty().append($tbl);
  });
});
