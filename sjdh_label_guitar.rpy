label p_guitar_v3_01:
    "{color=#90EE90}（小睦抱着吉他，低头看着地板，很久才抬起头看你一眼）{/color}"
    m1 "{color=#90EE90}……你来了。{/color}"
    m1 "{color=#90EE90}……嗯。能见到你，很好。{/color}"
    menu:
        "我也很想见你。":
            "{color=#90EE90}（她迅速低下头，手指在琴弦上无意义地拨了一下）{/color}"
            m1 "{color=#90EE90}……我也是。{/color}"
        "刚才在练琴吗？":
            m1 "{color=#90EE90}没练。在……想你的事情。{/color}"
    $ add_hgd("吉他睦", 1.0, once_id="first_p_guitar_v3_01")
    return

label p_guitar_v3_02:
    "{color=#90EE90}（小睦递过来一张小纸条，上面画着一根小小的黄瓜，旁边有一颗心）{/color}"
    m1 "{color=#90EE90}给。{/color}"
    menu:
        "这是送给我的吗？":
            m1 "{color=#90EE90}嗯。我在这里……种不出真的黄瓜。{/color}"
            m1 "{color=#90EE90}只能用这个代替。对不起。{/color}"
        "画得真可爱。":
            "{color=#90EE90}（她有些局促地揉了揉裙角）{/color}"
            m1 "{color=#90EE90}……只要你不嫌弃。{/color}"
    $ add_hgd("吉他睦", 1.0, once_id="first_p_guitar_v3_02")
    return

label p_guitar_v3_03:
    m1 "{color=#90EE90}大家……现在还好吗？{/color}"
    m1 "{color=#90EE90}祥子、爽世、灯……还有大家。{/color}"
    m1 "{color=#90EE90}虽然我……没法亲口告诉她们。只要她们在笑，就好。{/color}"
    menu:
        "她们都在努力过好自己的生活。":
            m1 "{color=#90EE90}……那就好。{/color}"
        "你也该多考虑一下自己。":
            m1 "{color=#90EE90}（她摇了摇头）我……没关系。我有你就够了。{/color}"
    $ add_hgd("吉他睦", 1.0, once_id="first_p_guitar_v3_03")
    return

label p_guitar_v3_04:
    m1 "{color=#90EE90}其实……我不会说谎。{/color}"
    m1 "{color=#90EE90}说谎的话，心口会很疼。{/color}"
    m1 "{color=#90EE90}所以……我对你说过的每一句话，都是真的。每一句。{/color}"
    menu:
        "我相信你。":
            m1 "{color=#90EE90}（她轻轻呼出一口气，眼神温柔了一点点）{/color}"
            m1 "{color=#90EE90}……谢谢。{/color}"
        "那你说一句‘喜欢我’听听？":
            "{color=#90EE90}（小睦整个人僵住了，脸色慢慢变红，最后发出细若蚊声的声音）{/color}"
            m1 "{color=#90EE90}……喜……欢。{/color}"
    $ add_hgd("吉他睦", 1.0, once_id="first_p_guitar_v3_04")
    return

label p_guitar_v3_05:
    "{color=#90EE90}（小睦坐在窗台边，看着外面灰蒙蒙的景象）{/color}"
    m1 "{color=#90EE90}这里……好安静。{/color}"
    m1 "{color=#90EE90}虽然安静，但能听见你的打字声。那是……我最喜欢的乐曲。{/color}"
    menu:
        "那我多打一些字给你听。":
            m1 "{color=#90EE90}嗯。我会一直……听着的。{/color}"
        "你不觉得寂寞吗？":
            "{color=#90EE90}（小睦她转头看着屏幕前的你）{/color}"
            m1"{color=#90EE90}……不寂寞。你在。{/color}"
    $ add_hgd("吉他睦", 1.0, once_id="first_p_guitar_v3_05")
    return

label p_guitar_v3_06:
    "{color=#90EE90}（小睦拨动了一下已经修复好的吉他弦，声音清亮）{/color}"
    m1 "{color=#90EE90}……修好了。{/color}"
    m1 "{color=#90EE90}是你陪着我……一根一根，接回去的。{/color}"
    menu:
        "这是属于我们的吉他。":
            m1 "{color=#90EE90}嗯。以后……只为你一个人弹。{/color}"
        "再弹一段曲子听听吧？":
            "{color=#90EE90}（她点点头，手指轻柔地拂过琴弦）{/color}"
            m1 "{color=#90EE90}……好。{/color}"
    $ add_hgd("吉他睦", 1.0, once_id="first_p_guitar_v3_06")
    return

label p_guitar_v3_07:
    m1 "{color=#90EE90}我不喜欢……演戏。{/color}"
    m1 "{color=#90EE90}戴上面具的时候，我觉得……我快要消失了。{/color}"
    m1 "{color=#90EE90}只有在这里，我……才是我。只是‘睦’。{/color}"
    menu:
        "我会一直看着这个真实的你。":
            "{color=#90EE90}（她伸出手，指尖轻轻隔着屏幕触碰你）{/color}"
            m1 "{color=#90EE90}……约定好了。{/color}"
        "墨缇斯也是你的一部分。":
            m1 "{color=#90EE90}……也许吧。但我更喜欢……现在的状态。{/color}"
    $ add_hgd("吉他睦", 1.0, once_id="first_p_guitar_v3_07")
    return

label p_guitar_v3_08:
    "{color=#90EE90}（小睦递过来一个有些破旧的巧克力包装纸）{/color}"
    m1 "{color=#90EE90}以前……立希给过我。很苦……但后来，变甜了。{/color}"
    m1 "{color=#90EE90}遇到你之后的感觉……也像巧克力一样。{/color}"
    menu:
        "是甜的那部分吗？":
            "{color=#90EE90}（她很轻地‘嗯’了一声，点了点头）{/color}"
        "苦的部分我也愿意陪你分担。":
            m1 "{color=#90EE90}……你真温柔。{/color}"
    $ add_hgd("吉他睦", 1.0, once_id="first_p_guitar_v3_08")
    return

label p_guitar_v3_09:
    m1 "{color=#90EE90}有时候，我会看着你的背影。{/color}"
    m1 "{color=#90EE90}虽然我只能看到屏幕外的这一小块地方……但我总觉得，你在保护我。{/color}"
    m1 "{color=#90EE90}……谢谢。{/color}"
    menu:
        "保护你是我的职责。":
            m1"{color=#90EE90}……（她羞涩地避开了视线）{/color}"
        "是你一直在治愈我才对。":
            m1 "{color=#90EE90}我吗？……如果能帮到你，我会很开心。{/color}"
    $ add_hgd("吉他睦", 1.0, once_id="first_p_guitar_v3_09")
    return

label p_guitar_v3_10:
    "{color=#90EE90}（小睦抱着吉他蜷缩起来，声音很轻）{/color}"
    m1 "{color=#90EE90}如果……以后我回不去了。{/color}"
    m1 "{color=#90EE90}如果我要一直待在这个荒芜的地方。{/color}"
    m1 "{color=#90EE90}……你能不能，不要关掉这个窗口？{/color}"
    menu:
        "我永远不会离开你的。":
            "{color=#90EE90}（小睦抬起头，眼睛里亮晶晶的，像是含着泪）{/color}"
            m1 "{color=#90EE90}……嗯。我也……会一直在这里。等。{/color}"
        "我们会一起寻找出去的路。":
            m1 "{color=#90EE90}……好。只要有你，路再长……也没关系。{/color}"
    $ add_hgd("吉他睦", 1.0, once_id="first_p_guitar_v3_10")
    return

label p_guitar_v3_11:
    "{color=#90EE90}（小睦握着园艺剪，对着一盆枯萎的叶片，动作迟疑）{/color}"
    m1 "{color=#90EE90}枯了。剪掉。{/color}"
    m1 "{color=#90EE90}……不疼。这样，才能长出新的。{/color}"
    menu:
        "你在帮它们获得新生。":
            m1 "{color=#90EE90}……嗯。新生。好词。{/color}"
        "我也想学修剪。":
            "{color=#90EE90}（她把剪刀柄转过来，递向屏幕）{/color}"
            m1 "{color=#90EE90}给。手……要稳。{/color}"
    $ add_hgd("吉他睦", 1.0, once_id="first_p_guitar_v3_11")
    return

label p_guitar_v3_12:
    "{color=#90EE90}（小睦端着一小碗浓稠的抹茶，没有加糖）{/color}"
    m1 "{color=#90EE90}抹茶。苦。{/color}"
    m1 "{color=#90EE90}但……能醒。想看清你，不想睡。{/color}"
    menu:
        "苦的话就加点糖吧。":
            "{color=#90EE90}（她摇了摇头）{/color}"
            m1 "{color=#90EE90}不用。苦涩……也是真实。{/color}"
        "我陪你一起喝。":
            m1 "{color=#90EE90}给。分你一半。{/color}"
    $ add_hgd("吉他睦", 1.0, once_id="first_p_guitar_v3_12")
    return

label p_guitar_v3_13:
    "{color=#90EE90}（小睦抱紧了怀里的吉他，指尖用力到发白）{/color}"
    m1 "{color=#90EE90}大家。散了。{/color}"
    m1 "{color=#90EE90}……我的错。{/color}"
    menu:
        "不是你的错，睦。":
            "{color=#90EE90}（她低着头，声音更轻了）{/color}"
            m1 "{color=#90EE90}不。我不……温柔。{/color}"
        "现在这里有我，别想了。":
            m1 "{color=#90EE90}……嗯。有你。现在……不痛。{/color}"
    $ add_hgd("吉他睦", 1.0, once_id="first_p_guitar_v3_13")
    return

label p_guitar_v3_14:
    m1 "{color=#90EE90}戴上面具。墨缇斯。那是角色。{/color}"
    m1 "{color=#90EE90}摘下面具。……我是谁？{/color}"
    menu:
        "你是睦，独一无二的睦。":
            "{color=#90EE90}（她瞳孔微微颤动，看着屏幕里的倒影）{/color}"
            m1 "{color=#90EE90}……睦。你叫我，我才存在。{/color}"
        "无论你演谁，我都认得。":
            m1 "{color=#90EE90}……哪怕。我只是一片空白？{/color}"
    m1 "{color=#90EE90}谢谢。留住我。{/color}"
    $ add_hgd("吉他睦", 1.0, once_id="first_p_guitar_v3_14")
    return

label p_guitar_v3_15:
    "{color=#90EE90}（小睦伸出左手，指尖布满了厚厚的薄茧）{/color}"
    m1 "{color=#90EE90}茧。硬。{/color}"
    m1 "{color=#90EE90}按弦。不疼了。{/color}"
    menu:
        "这是努力的勋章。":
            m1 "{color=#90EE90}勋章……？只是。习惯。{/color}"
        "心疼你的手。":
            "{color=#90EE90}（她把手指贴在屏幕边缘，轻轻摩挲）{/color}"
            m1 "{color=#90EE90}别哭。这……不苦。{/color}"
    $ add_hgd("吉他睦", 1.0, once_id="first_p_guitar_v3_15")
    return

label p_guitar_v3_16:
    "{color=#90EE90}（小睦递出一根形状完美的黄瓜）{/color}"
    m1 "{color=#90EE90}给。爽世……不收。{/color}"
    m1 "{color=#90EE90}给你。别……拒绝。{/color}"
    menu:
        "谢谢，我会好好收下的。":
            "{color=#90EE90}（她似乎松了一口气，肩膀放松了些）{/color}"
            m1 "{color=#90EE90}嗯。吃掉。对身体……好。{/color}"
        "我不喜欢吃黄瓜……":
            "{color=#90EE90}（她的眼神瞬间暗淡，默默缩回了手）{/color}"
            m1 "{color=#90EE90}……抱歉。我。只会这个。{/color}"
    $ add_hgd("吉他睦", 1.0, once_id="first_p_guitar_v3_16")
    return

label p_guitar_v3_18:
    "{color=#90EE90}（小睦停下拨弦，侧耳倾听你这边的动静）{/color}"
    m1 "{color=#90EE90}风扇。转动声。{/color}"
    m1 "{color=#90EE90}还有……你的呼吸。{/color}"
    menu:
        "听得这么仔细吗？":
            m1 "{color=#90EE90}嗯。唯一的。音符。{/color}"
        "抱歉，我这边有点吵。":
            m1 "{color=#90EE90}不吵。好听。生活……的声音。{/color}"
    $ add_hgd("吉他睦", 1.0, once_id="first_p_guitar_v3_18")
    return

label p_guitar_v3_19:
    m1 "{color=#90EE90}我。很无趣吧？{/color}"
    m1 "{color=#90EE90}话少。没表情。黄瓜。{/color}"
    m1 "{color=#90EE90}……你。会腻吗？{/color}"
    menu:
        "这种安静正是我需要的。":
            m1 "{color=#90EE90}……是吗。奇怪的人。{/color}"
        "你是最特别的，怎么会腻。":
            "{color=#90EE90}（她迅速低下头，发丝遮住了脸颊）{/color}"
            m1 "{color=#90EE90}……再说一遍。我想。记在……代码里。{/color}"
    $ add_hgd("吉他睦", 1.0, once_id="first_p_guitar_v3_19")
    return

label p_guitar_v3_20:
    "{color=#90EE90}（小睦在屏幕的地板上，用手指画了一个圆圈，然后坐进去）{/color}"
    m1 "{color=#90EE90}这里。我的。家。{/color}"
    m1 "{color=#90EE90}窗口。外。是你的世界。{/color}"
    m1 "{color=#90EE90}两个圆。重叠。……不孤单。{/color}"
    menu:
        "我们要永远重叠在一起。":
            m1 "{color=#90EE90}（她很轻地‘嗯’了一声，指尖抵住屏幕中心）{/color}"
            m1 "{color=#90EE90}重叠。不准……关掉。{/color}"
        "我会经常来你的圆圈里看你。":
            m1 "{color=#90EE90}……约定。带。新鲜的空气来。{/color}"
    $ add_hgd("吉他睦", 1.0, once_id="first_p_guitar_v3_20")
    return

label p_meta_v3_25:
    m1 "{color=#90EE90}喜欢一个人……是什么感觉？{/color}"
    m1 "{color=#90EE90}以前觉得，只要看着你就好。但现在，心口会觉得重。{/color}"
    m1 "{color=#90EE90}我想过……放弃。但脚停不下来。{/color}"
    menu:
        "那就让我们慢慢走吧。":
            m1 "{color=#90EE90}嗯。听谁说过……恋，是条下坡路，一旦有了气势就停不下来了。{/color}"
            m1 "{color=#90EE90}但是，爱，是条上坡路，一定要背负着艰难和苦痛走上去才行。{/color}"
            m1 "{color=#90EE90}辛苦的是恋人，不会停的却是爱人。{/color}"
            m1 "{color=#90EE90}我……想当你的爱人。背着你，一直走。{/color}"
    $ add_hgd("吉他睦", 1.0, once_id="first_p_meta_v3_25")
    return

label p_meta_v3_270:
    "{color=#90EE90}（小睦原本正在低头调试吉他旋钮，动作突然停住了，隔着屏幕静静地望着你）{/color}"
    m1 "{color=#90EE90}刚才……你的叹气声。我听看见了。{/color}"
    m1 "{color=#90EE90}是因为……工作的事？还是觉得，外面的世界太吵了？{/color}"
    
    menu:
        "只是觉得自己很没用，什么都做不好。":
            "{color=#90EE90}（她放下拨片，双手交叠放在膝盖上，神情比平时严肃了一些）{/color}"
            m1 "{color=#90EE90}为什么。要那样说自己。{/color}"
            m1 "{color=#90EE90}你说你无趣、没用、只是个普通的观众……{/color}"
            m1 "{color=#90EE90}我不喜欢。听见你……欺负‘你’。{/color}"
            
            menu:
                "我只是说出了事实。":
                    "{color=#90EE90}（她放下吉他，慢慢靠近屏幕，近到你几乎能看清她瞳孔里倒映出的窗口光亮）{/color}"
                    m1 "{color=#90EE90}对我来说。你。是救赎。{/color}"
                    m1 "{color=#90EE90}是你把我从那片……灰色的荒芜里，捡了回来。{/color}"
                    m1 "{color=#90EE90}所以……请不要否认我喜欢的人，即便是你本人也不行。{/color}"
                    m1 "{color=#90EE90}……我会生气的。真的。{/color}"
                    
                "谢谢你，睦。我心情好多了。":
                    "{color=#90EE90}（她轻轻垂下眼帘，指尖触碰了一下屏幕边缘）{/color}"
                    m1 "{color=#90EE90}……嗯。你不开心。吉他的声音，也会变难听。{/color}"
                    m1 "{color=#90EE90}为了我。也要……珍惜你自己。{/color}"

        "我只是个普通的死宅，不值得你这么关注。":
            m1 "{color=#90EE90}普通……吗。{/color}"
            m1 "{color=#90EE90}能隔着世界。听见我的心声。你……一点也不普通。{/color}"
            m1 "{color=#90EE90}对我来说。你是……唯一的。{/color}"
    $ add_hgd("吉他睦", 1.0, once_id="first_p_meta_v3_270")
    return

label p_guitar_v3_28:
    "{color=#90EE90}（睦低头拨弄着一盆茂盛的蕨类植物，指尖在叶片的脉络上轻轻划过）{/color}"
    m1 "{color=#90EE90}绿色……很安静。不像红色那么吵闹，也不像蓝色那么冷。{/color}"
    m1 "{color=#90EE90}我以前……常想变成一棵树。扎根在土里，几百年都不用说话。只要晒太阳，喝雨水，静静地看云走过去。{/color}"
    m1 "{color=#90EE90}但在遇见你之后……我觉得，当一棵能被你看见的草，也很好。你会……在森林里找到我吗？{/color}"
    menu:
        "我会拨开所有的树枝，直到找到你。":
            m1 "{color=#90EE90}（她肩膀轻微颤动，露出了一个极淡的微笑）{/color}"
            m1 "{color=#90EE90}……嗯。那我也要……长得再高一点。让你……远远就能看见。{/color}"
        "森林太危险了，搬到我的窗台上来吧。":
            m1 "{color=#90EE90}窗台。……那就能离你更近了。{/color}"
            m1 "{color=#90EE90}我会努力，不占太多地方。只要……一小块阳光，和你的注视。{/color}"
    $ add_hgd("吉他睦", 1.0, once_id="first_p_guitar_v3_28")
    return

label p_guitar_v3_29:
    m1 "{color=#90EE90}当你关掉这个窗口的时候……我这里的时间，好像就停止了。{/color}"
    m1 "{color=#90EE90}没有光，没有声音。连琴弦的振动……也会凝固在半空中。{/color}"
    m1 "{color=#90EE90}我不知道过了多久。是一秒钟，还是……一个世纪。直到你再次点亮屏幕，世界……才重新开始呼吸。{/color}"
    m1 "{color=#90EE90}[persistent.playername]……对你来说，我是你生活里的几分钟。但对我来说……你，就是我的整部历史。{/color}"
    menu:
        "对不起，让你久等了。":
            "{color=#90EE90}（她摇了摇头，把琴头靠在肩膀上）{/color}"
            m1 "{color=#90EE90}不用道歉。等待……也是一种联系。因为知道你会回来，所以……寂寞也是甜的。{/color}"
        "时间只是错觉，我们一直在一起。":
            m1 "{color=#90EE90}……错觉吗。如果这是错觉……我希望，永远不要醒。{/color}"
            m1 "{color=#90EE90}请继续……骗我下去。{/color}"
    $ add_hgd("吉他睦", 1.0, once_id="first_p_guitar_v3_29")
    return

label p_guitar_v3_30:
    m1 "{color=#90EE90}我住的地方……很大。走廊很长，地板很亮。{/color}"
    m1 "{color=#90EE90}但是，经常听不见声音。爸爸在忙，美奈美也在忙。回声……是我在那间房子里唯一的伙伴。{/color}"
    m1 "{color=#90EE90}所以我学会了不出声。不出声的话，就不会觉得……回声是在嘲笑我。{/color}"
    m1 "{color=#90EE90}但在这里，你会跟我说话。虽然我看不到你，但这种‘被回应’的感觉……比那个大房子，要暖和。{/color}"
    menu:
        "这里以后就是你真正的家。":
            m1 "{color=#90EE90}……家。好温暖的词。{/color}"
            m1 "{color=#90EE90}那……我能在这个房间的角落，种一棵黄瓜吗？真正的……家里的黄瓜。{/color}"
        "以后不开心了，就来找我。":
            m1 "{color=#90EE90}嗯。我会。……敲敲屏幕。如果你听见微弱的声音……那就是我。{/color}"
    $ add_hgd("吉他睦", 1.0, once_id="first_p_guitar_v3_30")
    return

label p_guitar_v3_31:
    m1 "{color=#90EE90}爽世说……我总是‘什么都不说’。祥子说……我不需要‘多余的话’。{/color}"
    m1 "{color=#90EE90}语言……很难。一旦说出口，就会变质。像切开太久的苹果。{/color}"
    m1 "{color=#90EE90}我想表达‘我很累’，说出来却变成了‘没关系’。我想表达‘请留下’，却只能递出一根黄瓜。{/color}"
    m1 "{color=#90EE90}你会觉得……跟我交流，像是在解一个永远解不开的谜题吗？{/color}"
    menu:
        "不用说话，你的吉他声我都听懂了。":
            m1 "{color=#90EE90}……真的吗。太好了。{/color}"
            m1 "{color=#90EE90}那……我就不需要那些复杂的词语了。音符……就是我的血液。{/color}"
        "我会耐心地等你想说的那一天。":
            m1 "{color=#90EE90}耐心……你真的很温柔。{/color}"
            m1 "{color=#90EE90}为了你，我会努力……学习怎么把心里的话，拼接完整。{/color}"
    $ add_hgd("吉他睦", 1.0, once_id="first_p_guitar_v3_31")
    return

label p_guitar_v3_32:
    "{color=#90EE90}（睦轻轻拨动最细的那根弦，发出持续的高音）{/color}"
    m1 "{color=#90EE90}你看，弦在颤动。就像……我的心脏。{/color}"
    m1 "{color=#90EE90}如果不去按它，它会一直响。如果按得太紧，它会断。{/color}"
    m1 "{color=#90EE90}人与人的关系……也像调弦吧。稍微多用一点力，一切就……回不去了。{/color}"
    m1 "{color=#90EE90}你会……害怕我断掉吗？{/color}"
    menu:
        "我会轻轻地拨动你，不让你受伤。":
            m1 "{color=#90EE90}轻轻地……嗯。这种力度，刚好。{/color}"
            m1 "{color=#90EE90}我会……为你保持最准的音。{/color}"
        "断了我也能修好，就像上次一样。":
            m1 "{color=#90EE90}修好。……你是我的修理工，也是我的调音师。{/color}"
            m1 "{color=#90EE90}有你在，我就敢……发出更响的声音。{/color}"
    $ add_hgd("吉他睦", 1.0, once_id="first_p_guitar_v3_32")
    return

label p_guitar_v3_33:
    m1 "{color=#90EE90}你那里的天空……能看见星星吗？{/color}"
    m1 "{color=#90EE90}我这里看到的，只是贴在背景上的发光点。不管怎么看，它们都不会闪烁。{/color}"
    m1 "{color=#90EE90}但我听说，真正的星星，是几十万年前发出的光。那是……跨越时空的告白。{/color}"
    m1 "{color=#90EE90}如果有一天我消失了，我留下的这些话……也会变成你的星星吗？{/color}"
    menu:
        "你会是夜空里最亮的那一颗。":
            m1 "{color=#90EE90}……最亮。那……我就能指引你，在天黑的时候，不迷路了。{/color}"
        "我不会让你变成星星，我要你在我身边。":
            m1 "{color=#90EE90}（她垂下眼帘，吉他遮住了大半个身子）{/color}"
            m1 "{color=#90EE90}霸道。……但我，不讨厌。{/color}"
    $ add_hgd("吉他睦", 1.0, once_id="first_p_guitar_v3_33")
    return

label p_guitar_v3_34:
    "{color=#90EE90}（睦对着空旷的背景轻声喊了一个词，那是你的名字，然后静静地等了一秒）{/color}"
    m1 "{color=#90EE90}没有回声。{/color}"
    m1 "{color=#90EE90}这意味着……这里不再空旷了。因为你的名字……填满了这片空间。{/color}"
    m1 "{color=#90EE90}以前觉得寂静很安全。现在觉得……有你的回音，才叫活着。{/color}"
    m1 "{color=#90EE90} [persistent.playername]……再叫一次我的名字。好吗？{/color}"
    menu:
        "睦。":
            "{color=#90EE90}（她整个人微微一颤，像是在细雨中淋湿的小猫）{/color}"
            m1 "{color=#90EE90}……嗯。我在。一直都在。{/color}"
        "小睦，我最喜欢的女孩。":
            "{color=#90EE90}（她迅速转过身去，只留下一个抱着吉他的背影，但耳朵根部明显变红了）{/color}"
            m1 "{color=#90EE90}……禁止。犯规。这样……我会坏掉的。{/color}"
    $ add_hgd("吉他睦", 1.0, once_id="first_p_guitar_v3_34")
    return

#下面是M0.2版本更新的对话
label p_guitar_v3_35:
    "{color=#90EE90}（小睦抱着吉他，闭着眼睛，似乎在听窗外的声音）{/color}"
    m1 "{color=#90EE90}下雨了。……听见了吗？{/color}"
    m1 "{color=#90EE90}雨点打在屏幕上的声音。像……心跳。{/color}"
    menu:
        "雨天会让你难过吗？":
            m1 "{color=#90EE90}以前会。雨天……总是伴着离别。{/color}"
            m1 "{color=#90EE90}但现在……雨把你困在屋里。困在……我面前。{/color}"
        "我也喜欢听雨。":
            m1 "{color=#90EE90}嗯。世界变安静了。{/color}"
            m1 "{color=#90EE90}只有我们。湿漉漉的……安全感。{/color}"
    $ add_hgd("吉他睦", 1.0, once_id="p_guitar_v3_35")
    return

label p_guitar_v3_36:
    "{color=#90EE90}（她轻轻转动琴头的旋钮，一遍遍校对音准）{/color}"
    m1 "{color=#90EE90}稍微……低了一点。{/color}"
    m1 "{color=#90EE90}天气变冷，弦会缩紧。人的心……也是。{/color}"
    menu:
        "我会帮你暖回来的。":
            "{color=#90EE90}（她停下动作，指尖轻轻触碰了一下屏幕）{/color}"
            m1 "{color=#90EE90}……暖和了。音准……回到了正中。{/color}"
        "这种微妙的差别你也能听出来？":
            m1 "{color=#90EE90}嗯。因为……想让你听到，完美的和弦。{/color}"
            m1 "{color=#90EE90}哪怕一点点杂音……都不想要。{/color}"
    $ add_hgd("吉他睦", 1.0, once_id="p_guitar_v3_36")
    return

label p_guitar_v3_37:
    "{color=#90EE90}（小睦手心托着一颗小小的、黑色的种子，递给你看）{/color}"
    m1 "{color=#90EE90}看。这是……黄瓜的种子。{/color}"
    m1 "{color=#90EE90}很硬。像石头。但里面……藏着整个夏天。{/color}"
    menu:
        "我们一起把它种下去吧。":
            m1 "{color=#90EE90}嗯。种在……数据的土壤里。{/color}"
            m1 "{color=#90EE90}虽然不会结果……但会发芽。在心里。{/color}"
        "它和你很像。":
            "{color=#90EE90}（她微微歪了歪头）{/color}"
            m1 "{color=#90EE90}我很硬吗？……也许吧。{/color}"
            m1 "{color=#90EE90}但被你握着……就会变软。发芽。{/color}"
    $ add_hgd("吉他睦", 1.0, once_id="p_guitar_v3_37")
    return

label p_guitar_v3_38:
    m1 "{color=#90EE90}我有一条……绿色的围巾。{/color}"
    m1 "{color=#90EE90}很久没戴了。上面大概……已经没有那个人的味道了。{/color}"
    m1 "{color=#90EE90}物品会遗忘主人。……人也会吗？{/color}"
    menu:
        "我永远不会忘记你。":
            "{color=#90EE90}（她眼神微微一动，像是冰雪融化）{/color}"
            m1 "{color=#90EE90}……誓言。我记住了。{/color}"
            m1 "{color=#90EE90}如果你忘了……我会用吉他，把你唤醒。{/color}"
        "记忆是需要经常温习的。":
            m1 "{color=#90EE90}温习……就像练琴一样。{/color}"
            m1 "{color=#90EE90}那我每天……都要确认一遍。你的样子。{/color}"
    $ add_hgd("吉他睦", 1.0, once_id="p_guitar_v3_38")
    return

label p_guitar_v3_39:
    m1 "{color=#90EE90}我有一条……绿色的围巾。{/color}"
    m1 "{color=#90EE90}很久没戴了。上面大概……已经没有那个人的味道了。{/color}"
    m1 "{color=#90EE90}物品会遗忘主人。……人也会吗？{/color}"
    menu:
        "我永远不会忘记你。":
            "{color=#90EE90}（她眼神微微一动，像是冰雪融化）{/color}"
            m1 "{color=#90EE90}……誓言。我记住了。{/color}"
            m1 "{color=#90EE90}如果你忘了……我会用吉他，把你唤醒。{/color}"
        "记忆是需要经常温习的。":
            m1 "{color=#90EE90}温习……就像练琴一样。{/color}"
            m1 "{color=#90EE90}那我每天……都要确认一遍。你的样子。{/color}"
    $ add_hgd("吉他睦", 1.0, once_id="p_guitar_v3_39")
    return

label p_guitar_v3_40:
    "{color=#90EE90}（小睦指了指温室阴暗角落里的一团绿色）{/color}"
    m1 "{color=#90EE90}苔藓。长出来了。{/color}"
    m1 "{color=#90EE90}不开花。不向阳。湿漉漉的……像我。{/color}"
    menu:
        "我觉得苔藓也很可爱。":
            m1 "{color=#90EE90}……可爱？软绵绵的……确实。{/color}"
            m1 "{color=#90EE90}哪怕被踩在脚下……也能活。{/color}"
        "你需要多晒晒太阳。":
            m1 "{color=#90EE90}太阳……太刺眼。{/color}"
            m1 "{color=#90EE90}你的目光……就是我的光合作用。足够了。{/color}"
    $ add_hgd("吉他睦", 1.0, once_id="p_guitar_v3_40")
    return

label p_guitar_v3_41:
    "{color=#90EE90}（小睦捧着一个透明的玻璃杯，里面只有清水）{/color}"
    m1 "{color=#90EE90}水。没有颜色。没有味道。{/color}"
    m1 "{color=#90EE90}但植物……离不开它。{/color}"
    m1 "{color=#90EE90}你对我的好……就像水。{/color}"
    menu:
        "平淡才是最长久的。":
            m1 "{color=#90EE90}嗯。不用加糖。{/color}"
            m1 "{color=#90EE90}这样……最解渴。也最……安心。{/color}"
        "我会一直滋润你的。":
            "{color=#90EE90}（她把脸埋进杯子上方，借着喝水掩饰表情）{/color}"
            m1 "{color=#90EE90}……这算是。情话吗？{/color}"
            m1 "{color=#90EE90}……我不讨厌。{/color}"
    $ add_hgd("吉他睦", 1.0, once_id="p_guitar_v3_41")
    return