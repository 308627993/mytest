def get_xml(type):
    xml_template='''
    <xml>
        <ToUserName><![CDATA[{{toUser}}]]></ToUserName>
        <FromUserName><![CDATA[{{fromUser}}]]></FromUserName>
        <CreateTime>{{createTime}}</CreateTime>
        <MsgType><![CDATA[{{type}}]]></MsgType>
        %s
    </xml>
    '''
    text_type = '<Content><![CDATA[{{content}}]]></Content>'
    image_type = '''
    <Image>
        <MediaId><![CDATA[{{media_id}}]]></MediaId>
    </Image>
    '''
    voice_type = '''
    <Voice>
        <MediaId><![CDATA[{{media_id}}]]></MediaId>
    </Voice>
    '''
    video_type = '''
    <Video>
        <MediaId><![CDATA[{{media_id}}]]></MediaId>
        <Title><![CDATA[{{title}}]]></Title>
        <Description><![CDATA[{{description}}]]></Description>
    </Video>
    '''
    music_type = '''
    <Music>
        <Title><![CDATA[{{TITLE}}]]></Title>
        <Description><![CDATA[{{DESCRIPTION}}]]></Description>
        <MusicUrl><![CDATA[{{MUSIC_Url}}]]></MusicUrl>
        <HQMusicUrl><![CDATA[{{HQ_MUSIC_Url}}]]></HQMusicUrl>
        <ThumbMediaId><![CDATA[{{media_id}}]]></ThumbMediaId>
    </Music>
    '''
    news_type = '''
    <ArticleCount>{{ article_cont }}</ArticleCount>
    <Articles>
        {% for i in news %}
        <item>
            <Title><![CDATA[{{ i.title1 }}]]></Title>
            <Description><![CDATA[{{ i.description1 }}]]></Description>
            <PicUrl><![CDATA[{{ i.picurl }}]]></PicUrl>
            <Url><![CDATA[{{ i.url }}]]></Url>
        </item>
        {% endfor %}
    </Articles>
    '''
    if type == 'text':
        return xml_template%(text_type)
    elif type == 'image':
        return xml_template%(image_type)
    elif type == 'voice':
        return xml_template%(voice_type)
    elif type == 'video':
        return xml_template%(video_type)
    elif type == 'music':
        return xml_template%(music_type)
    elif type == 'news':
        return xml_template%(news_type)
