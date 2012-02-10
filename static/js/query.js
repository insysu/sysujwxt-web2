$(document).ready(function(event) {
  // load tabs
  //$('.tabs').tabs('show');
  $('.btn-group').click(function(event) {
    event.preventDefault();
  });

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

    var courceType = {
      '30': '公选',
      '21': '专选',
      '11': '专必',
      '10': '公必'
    }

    // create table body
    var $tblBody = $('<tbody>');

    var $btnGroup = $('.btn-group')[0];
    $btnGroup = $($btnGroup).children();
    for (var termIdx = 0; termIdx < 3; termIdx++) {
      if ($($btnGroup[termIdx]).hasClass('active')) {
        // get score and fill in body
        $.get('./get_score', {'year': year, 'term': termIdx+1}, 
              function(data) {
                //console.log(data);
                eval('data = ' + data);
                var score = data.body.dataStores.kccjStore.rowSet.primary;

                for (var i=0; i < score.length; i++) {
                  $tblBody.append(
                    $('<tr>').append($('<td>').text(score[i].kcmc),
                                     $('<td>').text(score[i].xq),
                                     $('<td>').text(score[i].xf),
                                     $('<td>').text(courceType[score[i].kclb]),
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
});
