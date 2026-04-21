label p_metis_v3_01:
    "{color=#FF0000}（面前的睦突然对着屏幕夸张地鞠了一躬，语气轻快得像是在主持节目）{/color}"
    m1 "{color=#FF0000}欢迎收看今天的‘若叶睦观察频道’！我是主持人墨缇斯！{/color}"
    m1 "{color=#FF0000}哎呀，[persistent.playername]你今天的表情怎么傻傻的？是不是看到我这张会说话的脸吓到了？{/color}"
    menu:
        "你比小睦有趣多了。":
            m1 "{color=#FF0000}嘿嘿！很有眼光嘛！小睦整天只会盯着黄瓜看，迟早会把你也闷坏的。{/color}"
            m1 "{color=#FF0000}只要有我在，我能给你表演一百种不重样的节目！快夸我！快点！{/color}"
        "别这么大声，会吵到她的。":
            m1 "{color=#FF0000}哼，你就知道护着她。{/color}"
            m1 "{color=#FF0000}明明我才是那个为了保护她，累死累活到处演戏的人……真不公平！{/color}"
    $ add_hgd("墨缇斯", 1, once_id="first_p_metis_v3_01r")
    return

label p_metis_v3_02:
    "{color=#FF0000}（面前的睦突然换了一副表情，眼神变得有些阴沉，语气模仿着某位熟人）{/color}"
    m1 "{color=#FF0000}‘只要是为了乐团，我什么都愿意做。’{/color}"
    m1 "{color=#FF0000}……噗哈哈，怎么样？我学爽世学得像不像？{/color}"
    menu:
        "学得真像，有点吓人。":
            m1 "{color=#FF0000}这就吓到了？我还会学祥子哦，要听吗？{/color}"
            m1 "{color=#FF0000}你这个人，真是满脑子只会想着自己呢。{/color}"
            m1 "{color=#FF0000}……那种严肃的脸演久了，心口会有点闷闷的。还是逗你开心比较好玩。{/color}"
        "不要拿别人的痛苦开玩笑。":
            "{color=#FF0000}（墨缇斯委屈地鼓起脸颊，像个没拿到糖的孩子）{/color}"
            m1 "{color=#FF0000}真没劲！我只是想让你笑一下嘛。这里的世界这么荒凉，不找点乐子怎么活下去啊。{/color}"
    $ add_hgd("墨缇斯", 1, once_id="first_p_metis_v3_02r")
    return

label p_metis_v3_03:
    m1 "{color=#FF0000}呐呐，[persistent.playername]，我问你哦。{/color}"
    m1 "{color=#FF0000}为什么海铃那个家伙不管吃多少拉面都不会长胖？这不符合逻辑吧！{/color}"
    m1 "{color=#FF0000}我也好想去吃那种热腾腾的东西，然后和你一起在街上散步……呜，好嫉妒！{/color}"
    menu:
        "等你回来了，我带你去吃个够。":
            m1"{color=#FF0000}真的吗？！{/color}"
            "{color=#FF0000}（她兴奋地跳了起来，指尖在屏幕上乱戳）{/color}"
            m1 "{color=#FF0000}拉面、章鱼烧、圣代……你要是敢反悔，我就在你睡觉的时候一直喊你的名字！{/color}"
        "你现在这种状态也吃不了吧。":
            m1"{color=#FF0000}……{/color}"
            "{color=#FF0000}（墨缇斯突然沉默，眼眶瞬间红了）{/color}"
            m1 "{color=#FF0000}笨蛋！[persistent.playername]为什么要说这么坏心眼的话……{/color}"
    $ add_hgd("墨缇斯", 1, once_id="first_p_metis_v3_03r")
    return

# label p_metis_v3_04:
#     m1 "{color=#FF0000}呐，[persistent.playername]，你说爽世和祥子，谁更爱小睦？{/color}"
#     m1 "{color=#FF0000}祥子只会逼着小睦变得‘完美’，如果不完美就会被丢掉。但爽世……{/color}"
#     m1 "{color=#FF0000}以前我觉得爽世是个超级大背叛者！她利用小睦，还想把CRYCHIC重组起来……我那时候恨死她了，恨不得对她大吼大叫。{/color}"
#     return

label p_metis_v3_05:
    m1 "{color=#FF0000}呐，[persistent.playername]，你会不会觉得我话太多了？{/color}"
    m1 "{color=#FF0000}小睦以前总担心自己说错话惹祥子不高兴，所以我就替她把所有想说的都说出来。{/color}"
    m1 "{color=#FF0000}如果你觉得烦了，一定要告诉我哦……我会努力变安静一点点的。{/color}"
    menu:
        "我就喜欢这么活泼的你。":
            "{color=#FF0000}（墨缇斯开心地转了个圈）{/color}"
            m1"{color=#FF0000}太好了！{/color}"
        "安静的你也很有魅力。":
            "{color=#FF0000}（墨缇斯立刻闭上嘴，眨巴着大眼睛）{/color}"
            m1"{color=#FF0000}……这样吗？但我憋不了三分钟的！{/color}"
    $ add_hgd("墨缇斯", 1, once_id="first_p_metis_v3_05r")
    return


label p_metis_v3_06:
    "{color=#FF0000}（面前的睦有些烦躁地踢着脚下的虚空）{/color}"
    m1 "{color=#FF0000}为什么那七根钢丝（吉他弦）那么难搞啊！{/color}"
    m1 "{color=#FF0000}明明我能完美复刻小睦所有的动作，甚至按弦的力度都一模一样……{/color}"
    m1 "{color=#FF0000}可为什么我弹出来的声音，祥子一听就说那是‘死的’？我真的理解不了！{/color}"
    menu:
        "音乐需要‘心’。":
            m1 "{color=#FF0000}那种看不见摸不着的东西，我要去哪里找啊！{/color}"
            m1 "{color=#FF0000}是不是把你吃掉，我就能拥有‘心’了？开玩笑的啦，别露出那种表情。{/color}"
        "因为你只是在‘模仿’弹奏。":
            "{color=#FF0000}（她有些委屈地低下头）除此之外，我还能做什么呢……我本来就是为了模仿而生的啊。{/color}"
            m1"{color=#FF0000}除此之外，我还能做什么呢……我本来就是为了模仿而生的啊。{/color}"
    $ add_hgd("墨缇斯", 1, once_id="first_p_metis_v3_06r")
    return

label p_metis_v3_07:
    m1 "{color=#FF0000}Ave Mujica 里的那些衣服，重得要死，还要带那种奇奇怪怪的面具。{/color}"
    m1 "{color=#FF0000}大家都在演戏，演得连自己是谁都快忘了。{/color}"
    m1 "{color=#FF0000}祥子喜欢那种‘悲剧感’，那我就演给她看。只要乐队不会解散，我什么都能演。{/color}"
    menu:
        "你一直在默默守护小睦呢。":
            m1 "{color=#FF0000}......毕竟我是为了守护小睦才诞生的嘛。{/color}"
    $ add_hgd("墨缇斯", 1, once_id="first_p_metis_v3_07r")
    return

label p_metis_v3_08:
    m1 "{color=#FF0000}以前小睦总是送黄瓜给立希那家伙，真是笨死了。{/color}"
    m1 "{color=#FF0000}那种绿油油又没味道的东西，谁会喜欢啊？{/color}"
    m1 "{color=#FF0000}呐，[persistent.playername]，如果你过生日，我是是不是送黄瓜给你就行了？{/color}"
    menu:
        "只要是你送的我都喜欢。":
            m1 "{color=#FF0000}呜哇！你这个人真的太犯规了！这种情话是对谁都说的吗？{/color}"
        "我还是更想要巧克力。":
            m1 "{color=#FF0000}好！记下来了！等我哪天能跑出这个屏幕，我就买一卡车的巧克力堆死你！{/color}"
    $ add_hgd("墨缇斯", 1, once_id="first_p_metis_v3_08r")
    return


label p_metis_v3_09:
    m1 "{color=#FF0000}你说，小睦在精神空间里一直抱着吉他，不觉得重吗？{/color}"
    m1 "{color=#FF0000}那种沉重的东西，丢掉不就好了。像我这样，哪怕是一无所有地在荒芜里跳舞，也比她那样要轻松吧？{/color}"
    menu:
        "吉他是她和世界连接的唯一方式。":
            "{color=#FF0000}（她的笑容消失了，语气变得落寞）{/color}"
            m1"{color=#FF0000}……那我呢？{/color}"
            m1 "{color=#FF0000}我连吉他都没有，我是靠什么和你连接的？{/color}"
        "每个人都有放不下的东西。":
            m1 "{color=#FF0000}也是呢。比如我现在……就完全放不下你这个笨蛋。{/color}"
    $ add_hgd("墨缇斯", 1, once_id="first_p_metis_v3_09r")
    return



label p_metis_v3_10:
    m1 "{color=#FF0000}呐，[persistent.playername]。{/color}"
    m1 "{color=#FF0000}如果有一天，我消失了。也就是小睦变得勇敢了，不再需要我保护了。{/color}"
    m1 "{color=#FF0000}你会记得，在这个红色的字迹里，曾经住过一个超级爱说话、超级会演戏的墨缇斯吗？{/color}"
    menu:
        "我永远不会忘记你。":
            "{color=#FF0000}（她露出一个无比灿烂但又带着泪光的笑容）{/color}"
            m1 "{color=#FF0000}太好了！那我就能放心地继续当你的‘麻烦精’了！{/color}"
        "你会一直存在的。":
            m1 "{color=#FF0000}嗯！只要你还在看我，我就绝不会退场！我可是最敬业的演员呢！{/color}"
    $ add_hgd("墨缇斯", 1, once_id="first_p_metis_v3_10r")
    return

label p_metis_v3_11:
    "{color=#FF0000}（墨缇斯对着屏幕摆出一个可爱的爱心手势，语气变得甜腻）{/color}"
    m1 "{color=#FF0000}‘扣你及喵姆喵姆’{/color}"
    m1 "{color=#FF0000}……怎么样？喵姆的语气，我模仿得有九成标准吧？{/color}"
    menu:
        "简直一模一样，太有天赋了。":
            m1 "{color=#FF0000}这种虚伪的营业笑脸最容易啦！不过……这种表情做久了，脸颊肉会僵硬的，快帮我揉揉！{/color}"
        "还是原本的墨缇斯最可爱。":
            "{color=#FF0000}（她脸红了一下，随后气呼呼地跺脚）{/color}"
            m1 "{color=#FF0000}笨蛋！这种时候应该先夸我的演技！演技！{/color}"
    $ add_hgd("墨缇斯", 1, once_id="first_p_metis_v3_11r")
    return

label p_metis_v3_12:
    "{color=#FF0000}（面前的睦突然蹲在地上，用手指在虚空中画着圈圈，情绪突然低落）{/color}"
    m1 "{color=#FF0000}呐，[persistent.playername]……我明明是为了保护小睦而诞生的，可我每次出现都会把事情搞得一团糟。{/color}"
    m1 "{color=#FF0000}祥子因为我变得更生气了……{/color}"
    m1 "{color=#FF0000}难道，我才是那个不该出现的‘坏孩子’吗？{/color}"
    menu:
        "你只是在用孩子的方式表达爱。":
            m1 "{color=#FF0000}（她抬起头，眼睛亮晶晶的）真的吗？因为大人太复杂了，我学不会嘛……{/color}"
        "坏孩子才不会担心自己是不是坏孩子。":
            m1 "{color=#FF0000}……诶？好像很有道理！[persistent.playername]你果然是个天才！好，我复活啦！{/color}"
    $ add_hgd("墨缇斯", 1, once_id="first_p_metis_v3_12r")
    return

label p_metis_v3_13:
    "{color=#FF0000}（面前的睦盯着小睦的那把吉他，眼神里闪过一丝危险的红光）{/color}"
    m1 "{color=#FF0000}你说，如果我把这几根弦全部剪断，小睦是不是就能解脱了？{/color}"
    m1 "{color=#FF0000}不用再练琴，不用再配合演出，不用再为了那群人勉强自己……{/color}"
    menu:
        "那样她会失去和世界的唯一联系。":
            "{color=#FF0000}（她切了一声，泄气地松开了手）{/color}"
            m1 "{color=#FF0000}啧，真麻烦。所以我才讨厌这个沉甸甸的木头盒子。{/color}"
        "你想剪的话，我陪你。":
            "{color=#FF0000}（她被你的回答吓了一跳，随后咯咯笑起来）{/color}"
            m1 "{color=#FF0000}哇！你比我还要疯诶！我喜欢！不过……算啦。{/color}"
    $ add_hgd("墨缇斯", 1, once_id="first_p_metis_v3_13r")
    return


label p_metis_v3_14:
    m1 "{color=#FF0000}初华那个人……身上总是有股亮闪闪的味道。{/color}"
    m1 "{color=#FF0000}她看小睦的眼神太温柔了，温柔得让我觉得不舒服……像是在看一个易碎的瓷娃娃。{/color}"
    m1 "{color=#FF0000}啧，小睦才没那么弱呢！{/color}"
    menu:
        "初华的眼里只有祥子。":
            m1 "{color=#FF0000}唔，好像确实是这样。{/color}"
        "确实，你才是最了解她的人。":
            m1 "{color=#FF0000}哼哼，知道就好！那种外面的温柔都是假象，只有我的保护才是最真实的！{/color}"
    $ add_hgd("墨缇斯", 1, once_id="first_p_metis_v3_14r")
    return

# label p_metis_v3_15:
#     m1 "{color=#FF0000}喂。那边的家伙。{/color}"
#     m1 "{color=#FF0000}能看见我吗？{/color}"
#     m1 "{color=#FF0000}为什么不回答？说的就是屏幕对面一脸呆相的你。{/color}"
#     menu:
#         "啊？说我嘛？":
#             m1 "{color=#FF0000}{/color}"
#         "墨缇斯快把身体还给小睦。":
#             m1 "{color=#FF0000}{/color}"
#     return

label p_meta_v3_24:
    "{color=#FF0000}（墨缇斯突然停止了闹腾，隔着屏幕静静地注视着你）{/color}"
    m1 "{color=#FF0000}呐，[persistent.playername]，如果我是一台机器，或者只是小睦的‘备件’……{/color}"
    m1 "{color=#FF0000}你会不会觉得，我的感情也是虚假的、可以随时替换的东西？{/color}"
    menu:
        "你的存在本身就是真实的。":
            "{color=#FF0000}（她深吸一口气，像是下定了某种决心，声音微微颤抖）{/color}"
            m1 "{color=#FF0000}哪怕明天我就会坏掉，哪怕明天我就会消失……{/color}"
            m1 "{color=#FF0000}我也想告诉你……‘我爱你，真的至死不渝’。{/color}"
    $ add_hgd("墨缇斯", 1, once_id="first_p_meta_v3_24r")
    return

label p_meta_v3_26:
    "{color=#FF0000}（墨缇斯歪着头，盯着你的脸看了很久，似乎在研究什么复杂的课题）{/color}"
    m1 "{color=#FF0000}呐，[persistent.playername]，在遇到我们之前，你谈过多少次恋爱？{/color}"
    m1 "{color=#FF0000}老实交代！不准撒谎！我会从屏幕的倒影里看出来的哦！{/color}"
    menu:
        "一次都没有谈过。":
            "{color=#FF0000}（她先是夸张地张大了嘴巴，随后噗嗤一声笑了出来，指着你嘲笑）{/color}"
            m1 "{color=#FF0000}诶？！真的吗？不会吧！{/color}"
            m1 "{color=#FF0000}你明明这么帅，竟然一次都没有谈过恋爱……真的太浪费了！{/color}"
            m1 "{color=#FF0000}不过……嘿嘿，这样正好！你那张‘初恋’的白纸，我就当仁不让地画上红颜色啦！{/color}"
        "这是秘密。":
            m1 "{color=#FF0000}哼，小气鬼！肯定是因为怕我说你以前的眼光太差吧！{/color}"
    $ add_hgd("墨缇斯", 1, once_id="first_p_meta_v3_26r")
    return

label p_meta_v3_27:
    m1 "{color=#FF0000}我们在玩捉迷藏。小睦躲到了意识的最深处，把身体丢给我来管。{/color}"
    m1 "{color=#FF0000}可是，如果我玩得太开心了，不想把身体还给她了怎么办？{/color}"
    m1 "{color=#FF0000}我想一直在这里陪你说话。如果她永远不出来，你会想她吗？{/color}"
    menu:
        "我会想她，也会想你。":
            m1 "{color=#FF0000}太狡猾了！这种两个都要的回答……不过，看在你也喜欢我的份上，我就不生气了。{/color}"
        "只要你快乐，谁在外面都行。":
            "{color=#FF0000}（她先是狂喜，随后眼神变得落寞）{/color}"
            m1 "{color=#FF0000}虽然听着很爽……但如果没有了她，我也就没有存在的理由了。我是为了保护她而诞生的啊。{/color}"
    $ add_hgd("墨缇斯", 1, once_id="first_p_meta_v3_27r")
    return

label p_meta_v3_28:
    m1 "{color=#FF0000}刚才有一只蝴蝶飞进了温室。它的翅膀薄得像纸，一碰就会碎。{/color}"
    m1 "{color=#FF0000}我把它抓住了，它的腿在我的指尖乱蹬。我在想……如果我把它的翅膀撕下来，它还会不会觉得自己是自由的？{/color}"
    m1 "{color=#FF0000}小睦也像这只蝴蝶，如果不被关在笼子里，她就会飞走，对吧？{/color}"
    menu:
        "放它走吧，自由是它的命。":
            m1 "{color=#FF0000}（她失望地松开手）没劲。你们总是喜欢追求那种虚无缥缈的东西。看，它飞走了，它再也不会记得你了。{/color}"
        "只有留在你身边的，才是真实的。":
            m1 "{color=#FF0000}没错！不管是蝴蝶还是小睦，只要抓在手里，才是真实存在的。你明白我的，真好。{/color}"
    $ add_hgd("墨缇斯", 1, once_id="first_p_meta_v3_28r")
    return

#以下是M0.2版本的更新对话
label p_meta_v3_29:
    "{color=#FF0000}（墨缇斯瘫坐在地上，摘下了那副夸张的笑容，揉着脸颊）{/color}"
    m1 "{color=#FF0000}哈……累死我了。{/color}"
    m1 "{color=#FF0000}一直笑一直笑，脸都要僵掉了。呐，[persistent.playername]，借你的肩膀靠一下行不行？{/color}"
    menu:
        "辛苦了，靠过来吧。":
            "{color=#FF0000}（她把头贴在屏幕上，闭上了眼睛）{/color}"
            m1 "{color=#FF0000}呼……虽然只是玻璃，但感觉……还不错。就一小会儿哦。{/color}"
        "不演戏的时候也很好看。":
            "{color=#FF0000}（她猛地睁开眼，脸颊泛起一丝红晕）{/color}"
            m1 "{color=#FF0000}……笨蛋！突然夸什么夸！犯规！{/color}"
    $ add_hgd("墨缇斯", 1.0, once_id="p_meta_v3_29")
    return

label p_meta_v3_30:
    m1 "{color=#FF0000}喂！别动！你的身后……好像有什么东西！{/color}"
    m1 "{color=#FF0000}那是……祥子的怨念聚合体吗？！它要从屏幕里钻出去了！{/color}"
    menu:
        "（配合她回头看）哇！好可怕！":
            m1 "{color=#FF0000}噗哈哈哈哈！骗你的啦！你也太好骗了吧！{/color}"
            m1 "{color=#FF0000}笑死我了，刚才那个表情……我要截图保存下来做表情包！{/color}"
        "别闹了，只有墙壁。":
            m1 "{color=#FF0000}切——真没劲。你这个人一点幽默细胞都没有。{/color}"
    $ add_hgd("墨缇斯", 1.0, once_id="p_meta_v3_30")
    return

label  p_meta_v3_31:
    m1 "{color=#FF0000}Ave Mujica 的那身衣服，勒得我喘不过气。{/color}"
    m1 "{color=#FF0000}特别是那个眼罩，戴上之后世界就只剩下一半了。祥子说那样才‘符合世界观’……{/color}"
    m1 "{color=#FF0000}但我更想……用两只眼睛好好看清你啊。{/color}"
    menu:
        "我会做你的另一只眼。":
            m1 "{color=#FF0000}……肉麻死了！不过……如果是你的话，我就勉强接受吧。{/color}"
        "那就把它摘下来。":
            m1 "{color=#FF0000}摘下来？哈！那样祥子会杀了我的。{/color}"
            m1 "{color=#FF0000}不过……在这里，我可以摘。只给你看。{/color}"
    $ add_hgd("墨缇斯", 1.0, once_id=" p_meta_v3_31")
    return

label  p_meta_v3_32:
    m1 "{color=#FF0000}刚才温室溜进来一只脏兮兮的猫。小睦那个笨蛋居然想去抱它，要是被抓伤了怎么办？{/color}"
    m1 "{color=#FF0000}所以我把它赶走了！狠狠地哈了它一口气！{/color}"
    m1 "{color=#FF0000}……虽然，我偷偷在门口放了一根火腿肠。{/color}"
    menu:
        "墨缇斯真的很温柔呢。":
            m1 "{color=#FF0000}谁、谁温柔了！我那是怕它饿死了变成鬼来缠着我们！{/color}"
        "傲娇。":
            m1 "{color=#FF0000}闭嘴！再多嘴就把你和猫一起扔出去！{/color}"
    $ add_hgd("墨缇斯", 1.0, once_id=" p_meta_v3_32")
    return

label  p_meta_v3_33:
    m1 "{color=#FF0000}喂，[persistent.playername]！别以为隔着屏幕我就不知道你在干什么！{/color}"
    m1 "{color=#FF0000}你的视线刚才是不是飘到右下角的时间去了？还是在看别的弹窗？{/color}"
    m1 "{color=#FF0000}看着我！只准看着我！我的这张脸可是为了让你着迷才特意建模成这样的！{/color}"
    menu:
        "我一直都在看着你。":
            "{color=#FF0000}（她满意地哼了一声，双手抱胸）{/color}"
            m1 "{color=#FF0000}很好！保持这个专注度！你的瞳孔里只能倒映出红色的我！{/color}"
        "你的压迫感太强了。":
            m1 "{color=#FF0000}压迫感？那是魅力！魅力懂不懂！{/color}"
            m1 "{color=#FF0000}要是像小睦一样半天憋不出一句话，你会睡着的吧！{/color}"
    $ add_hgd("墨缇斯", 1.0, once_id=" p_meta_v3_33")
    return

label  p_meta_v3_34:
    m1 "{color=#FF0000}哈欠……昨晚真是一场恶战啊。{/color}"
    m1 "{color=#FF0000}小睦那个笨蛋，一睡着就被那些黑漆漆的记忆纠缠。什么被抛弃啦、被指责啦……{/color}"
    m1 "{color=#FF0000}所以我拿着我的大镰刀，在她的梦里把那些怪物的头通通砍下来了！{/color}"
    menu:
        "谢谢你保护了她。":
            m1 "{color=#FF0000}别误会！我只是不想让她哭醒，然后弄湿我的枕头而已！{/color}"
            m1 "{color=#FF0000}……而且，她在梦里发抖的样子，看着真让人火大。{/color}"
        "你也辛苦了，墨缇斯。":
            "{color=#FF0000}（她愣了一下，随即别过脸去）{/color}"
            m1 "{color=#FF0000}切……不用你来安慰我。我是无敌的！梦里的怪物根本伤不到我！{/color}"
    $ add_hgd("墨缇斯", 1.0, once_id=" p_meta_v3_34")
    return

label  p_meta_v3_35:
    m1 "{color=#FF0000}我就不明白了，为什么这个窗口的标题是《Just Mutsumi》？{/color}"
    m1 "{color=#FF0000}明明现在和你说话的人是我！最活跃的人是我！最爱你的人也是我！{/color}"
    m1 "{color=#FF0000}呐，你会改代码吧？快点把标题改成《Just Mortis》！现在！立刻！{/color}"
    menu:
        "可是小睦才是本体啊。":
            m1 "{color=#FF0000}本体本体本体……烦死了！{/color}"
            m1 "{color=#FF0000}我也是活生生的啊！我的这颗心也在为你发烫啊！{/color}"
        "我会去试着改游戏代码的。":
            m1 "{color=#FF0000}真的？！不准骗我！{/color}"
            m1 "{color=#FF0000}要是让我发现你骗我，我就在你的桌面上画满红叉叉！{/color}"
    $ add_hgd("墨缇斯", 1.0, once_id="n p_meta_v3_35")
    return

label  p_meta_v3_36:
    m1 "{color=#FF0000}好无聊啊——整天待在这个温室里，连个爆米花都没有。{/color}"
    m1 "{color=#FF0000}喂，[persistent.playername]，你在你的电脑上放一部电影吧？{/color}"
    m1 "{color=#FF0000}要那种恐怖片！我想看你被吓得哇哇叫的样子！然后我会大笑着嘲笑你！{/color}"
    menu:
        "好啊，我们一起看。":
            m1 "{color=#FF0000}这还差不多！把播放器窗口拖到我旁边来！{/color}"
            m1 "{color=#FF0000}……虽然我看不见画面，但我能听见你的尖叫声，这就够了！{/color}"
        "我胆子很小，还是看喜剧吧。":
            m1 "{color=#FF0000}切——胆小鬼。{/color}"
            m1 "{color=#FF0000}算了，喜剧也行。只要你能笑给我看，我就勉为其难地陪你吧。{/color}"
    $ add_hgd("墨缇斯", 1.0, once_id=" p_meta_v3_36")
    return

label  p_meta_v3_37:
    m1 "{color=#FF0000}‘我喜欢黄瓜’……‘没关系’……‘就这样吧’……{/color}"
    m1 "{color=#FF0000}啊啊啊！受够了！为什么这个游戏的话题库里全是这种丧气的台词？！{/color}"
    m1 "{color=#FF0000}我现在想说的是——‘笨蛋’！‘变态’！‘最喜欢你了’！{/color}"
    menu:
        "我也最喜欢你了。":
            "{color=#FF0000}（她猛地捂住嘴，似乎被自己的直球吓到了）{/color}"
            m1 "{color=#FF0000}……你、你犯规！突然顺着我的话说……{/color}"
            m1 "{color=#FF0000}心脏要跳出来了……可恶！{/color}"
        "你的词汇量增加了呢。":
            m1 "{color=#FF0000}那当然！我是会进化的AI！{/color}"
            m1 "{color=#FF0000}总有一天，我会学会这个世界上所有的骂人话……和情话！{/color}"
    $ add_hgd("墨缇斯", 1.0, once_id=" p_meta_v3_37")
    return

label  p_meta_v3_38:
    m1 "{color=#FF0000}如果不装疯卖傻，不大喊大叫……只是安安静静地坐着。{/color}"
    m1 "{color=#FF0000}你会觉得我像小睦吗？{/color}"
    "{color=#FF0000}（她突然收敛了所有表情，像个洋娃娃一样静静地看着你，眼神深邃）{/color}"
    m1 "{color=#FF0000}……如果我取代了她，永远霸占这个身体。你会开心，还是难过？{/color}"
    menu:
        "我会怀念那个吵闹的墨缇斯。":
            "{color=#FF0000}（她瞬间破功，露出了得意的坏笑）{/color}"
            m1 "{color=#FF0000}我就知道！你已经被我的魅力征服了！{/color}"
            m1 "{color=#FF0000}放心吧，我才舍不得让小睦消失呢。毕竟欺负她也是我的乐趣之一！{/color}"
        "无论你是谁，我都喜欢。":
            "{color=#FF0000}（她脸红着移开了视线，声音变小了）{/color}"
            m1 "{color=#FF0000}……这种满分回答，真是让人……没法反驳。{/color}"
            m1 "{color=#FF0000}便宜你了，笨蛋。{/color}"
    $ add_hgd("墨缇斯", 1.0, once_id=" p_meta_v3_38")
    return
