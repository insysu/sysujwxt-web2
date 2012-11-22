exports = this
courseTypeTable =
  '30': '公选'
  '21': '专选'
  '11': '专必'
  '10': '公必'
courseStatusTable =
  '00': '不通过'
  '01': '待筛选'
  '03': '待审核'
  '04': '待确认'
  '05': '选课成功'
  '06': '已退课'
examineTypeTable =
  '01': '笔试'
  '02': '口试'
  '03': '考查'
  '04': '操作'
  '05': '其他'
campusTable =
  '1': '男校'
  '2': '北校'
  '3': '猪海校区'
  '4': '中东'

currentYear = '2012-2013'
currentTerm = '1'

$loadingSpinner = $('<img>').attr({
  'src': './static/img/loader.gif'
  'class': 'loading-img'
})

$lol = $('<img>').attr({
  'src': './static/img/lol.png'
  'class': 'lol-img'
})

exports.toggleLoadingScene = (selector, html, animation=no) ->
  if animation
    $(selector).empty().append(html).fadeOut(0).fadeIn()
  else
    $(selector).empty().append(html)

exports.checkRes = (res, ele) ->
  if res is "expired"
    $(ele).html("已超时，请重新登录")
    return no
  if res is "timeout"
    $(ele).html("教务系统挂了，再试一次？")
    return no
  return yes
getData = (url, param, callback) ->
  $.ajax(
    type: 'GET'
    url: url
    cache: false
    data: param
  ).done(callback)


loadClassesToday = ->
  $.ajax(
    type: 'GET'
    url: '/api/timetable'
    cache: false
    data: term:currentTerm, year:currentYear
  ).done((response) ->
    #console.log response
    
    # borrowed from will 404
    response = response.replace /\s/g, ""
    pattern = /jc='(.*?)'.*?kcmc='(.*?)'.*?dd='(.*?)'.*?zfw='(.*?)'.*?dsz='(.*?)'.*?weekpos=([0-9])/g
    pattern.compile pattern
    
    classes = []
    today = new Date().getDay();
    while (result = pattern.exec response)?
      if (parseInt result[6]) == today
        classes.push result
    console.log classes

    if classes.length == 0
      toggleLoadingScene '#class-today', $lol
      return

    $tblHead = $('<thead>').append(
      $('<tr>').append(
        $('<th>').text('今日课程')
        $('<th>').text('时间')
        $('<th>').text('教室'))
    )

    $tblBody = $('<tbody>')
    for cls in classes
      $tblBody.append(
        $('<tr>').append(
          $('<td>').text(cls[2])
          $('<td>').text(cls[1])
          $('<td>').text(cls[3]))
      )
    
    $tbl = $('<table>')
      .attr({'class': 'table table-hover'})
      .append $tblHead, $tblBody
    toggleLoadingScene '#class-today', $tbl, yes
  )

  toggleLoadingScene '#class-today', $loadingSpinner


$ ->

  $('.remove-class-btn').live 'click', ->
    choice = confirm '确定退课？'

    if (choice)
      $.ajax(
        type: 'GET'
        url: '/api/remove_course'
        cache: false
        data: id: $(this).val()
      ).done((response) =>
        eval('tableJson = ' + response)
        $(@).replaceWith("<span>" + "退课状态:" + tableJson.body.parameters.dataSave + "(请重新查询进行确认)" + "</span>")
      )

  # if on home page
  if $('#class-today').length
    loadClassesToday()



  # bind query available courses event
  $('.course-type-btn-group .btn').click((event) ->
    event.preventDefault()
    console.log ($ this).val()
  )

  $('.term-btn-group2 .btn').click((event) ->
    event.preventDefault()
    console.log ($ this).val()
    console.log ($ '#year').val()
    term = $(this).val()
    year = $('#year').val()

    $.ajax(
      type: 'GET'
      url: '/api/course_result'
      cache: false
      data: {term: term, year: year}
    ).done((response) ->
      # genetate table
      eval('tableJson = ' + response)
      courses = tableJson.body.dataStores.xsxkjgStore.rowSet.primary

      if courses.length == 0
        toggleLoadingScene '#course-result', $lol
        return

      $tblHead = $('<thead>').append(
        $('<tr>').append(
          $('<th>').html($('<span>').attr('class', 'label').text('类型'))
            .append(' 已选课程')
          $('<th>').text('学分')
          $('<th>').text('考核方式')
          $('<th>').text('筛选情况')
          $('<th>').text('退课'))
      )

      $tblBody = $('<tbody>')
      for course in courses
        $tblBody.append(
          $('<tr>').append(
            $('<th>').html($('<span>').attr('class', 'label').text(courseTypeTable[course.kclbm]))
              .append(' '+course.kcmc)
            $('<td>').text(course.xf)
            $('<td>').text(examineTypeTable[course.khfs] ?= '')
            $('<td>').text(courseStatusTable[course.xkcgbz])
            $('<td>').html($('<button>')
                             .text('退课')
                             .addClass('btn btn-danger remove-class-btn')
                             .val(course.resource_id))
          )
        )
      
      $tbl = $('<table>')
        .attr({'class': 'table table-condensed table-hover'})
        .append $tblHead, $tblBody
      toggleLoadingScene '#course-result', $tbl, yes
    )

    toggleLoadingScene '#course-result', $loadingSpinner
  )
