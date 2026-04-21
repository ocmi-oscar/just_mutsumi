define mc = Character("[player]", color="#6CA6CD") 
define mu1 = Character("若叶睦", color="#8FBC8F", who_outlines=[(2, "#2F4F2F")])
define mu0 = Character("月之森的不可思议女孩", color="#8FBC8F", who_outlines=[(2, "#2F4F2F")])
define mu2 = Character("若叶睦？", color="#8FBC8F", who_outlines=[(2, "#2F4F2F")])
label prologue_part0:
    
    jump sjdh

label prologue_part1:
    # --- 电影化章节字卡 (Cinematic Title Card) ---
    scene black
    pause 2.0
    
    # 极简的白字，缓慢浮现，带有呼吸感
    show text "{size=28}{space=10}Prologue{/size}\n\n{size=60}{font=fonts/cinematic.ttf}Down the Rabbit Hole{/font}{/size}\n\n{size=36}土中之呼吸 (De Profundis){/size}" at truecenter with Dissolve(2.5)
    pause 4.0
    hide text with Dissolve(2.0)
    pause 1.5
    # --- 极其自然的虚假动机 (Auto-Rationalization) ---
    play sound "audio/story/underwater_muffled.ogg" volume 0.4
    mc "（十月十五日。星期一。……大概吧。）"
    mc "（这是我人生中第一次，为了一块效果器去打工。）"
    mc "（Boss DD-8数字延迟——市价三万八千日元。对于一个靠着零用钱过活的人来说，这是一笔天文数字。）"
    mc "（但是......我想要。非常、非常想要。）"
    # 【修改点1】删掉“记忆模糊”，改成“对吉他的无理由狂热”，用普通人的本能来掩盖睦的潜意识。
    mc "（其实我没加过轻音部，没组过乐队，甚至连一把像样的电吉他都还没有。）"
    mc "（但就是想要。简直像某种……刻在骨子里的本能。）"
    mc "（只要闭上眼睛，脑子里全是那种声音。那种在深夜的房间里，一个人戴着耳机，让延迟的音符把所有的噪音和痛苦都隔绝在外的感觉。）"
    stop sound fadeout 3.0
    mc "（为此，我在求职网站上翻了整整一周，最后找到了这个——）"
    mc "（『月之森女子学园·旧校舍环境维护·短期兼职·时薪1100日元』）"
    # 【修改点2】删掉“敞开大门”的诡异感，改成打工人的“自我说服”。
    mc "（名门女校的管理，出乎意料地松散。）"
    mc "（我在求职网站上随便填了填资料，连线上面试都省了，第二天就直接拿到了电子通行证。）"
    mc "（不过想想也正常。这种又偏僻又脏、连正规园艺公司都不愿意接的废弃温室，外包公司能抓到一个愿意干体力活的廉价劳动力，大概高兴还来不及吧。）"
    mc "（唯一的问题是......评论区里，前任打工者留下的差评。）"
    scene white with Dissolve(0.2)
    show text "{size=26}「那地方......空气是死的」\n「干了三天就辞职了，受不了那种压迫感」\n「建议受不了低气压的人别去」{/size}" at truecenter with dissolve
    pause 4.0
    hide text with dissolve
    scene black with Dissolve(0.5)
    mc "（当时我还笑了。）"
    mc "（心想：现在的年轻人，真是经不起考验啊。不就是废弃建筑吗？顶多有点灰尘和蜘蛛网。）"
    mc "（我甚至觉得，这些夸张的评论，反而帮我筛掉了竞争者。）"
    mc "（......）"
    mc "（那时候的我，还不知道。）"
    mc "（我即将遇到的......不是什么超自然现象。）"
    mc "（而是一个，比任何幽灵都要难以触碰的人。）"
    # --- 场景1: 抵达月之森 ---
    scene bg_school_gate_dusk with fade
    play music story1 fadein 3.0 loop volume 0.7
    mc "……终于到了。"
    mc "（十月的黄昏，空气里混着烧焦的草味和远处电车的金属摩擦声。）"
    mc "（山手线沿线的富人区，月之森女子学园——光听名字就知道，这是和我这种普通人完全不同次元的地方。）"
    mc "（校门口的铜牌上，刻着学校的校训。）"
    mc "『あなたの輝きが道を照らす』（你的光芒会照亮前行之路）"
    mc "（......听起来就很贵。）"
    mc "（门口停着几辆漆黑的私家车。穿着考究制服的女学生们，谈笑着钻进车里，举手投足间带着一种浑然天成的从容。）"
    mc "（她们谈笑的声音很轻。但在我听来，却像隔着一层厚厚的水膜，带着一种不真实的距离感。）"
    mc "（这就是......所谓的『上流社会』吧。）"
    mc "（那是和我这种挤电车、在便利店挑最便宜饭团的人，截然不同的生态系统。）"
    mc "（......）"
    mc "（我低头看了看脖子上挂着的廉价塑料牌。）"
    show item_id_card at truecenter with dissolve:
        zoom 1.5
        linear 2.0 zoom 1.0
    pause 1.5
    hide item_id_card with dissolve
    mc "『月之森女子学园·旧校舍特别环境维护员（临时）』"
    mc "（翻译成大白话就是：正规园艺公司嫌太偏没人愿意接的脏活，廉价外包给想赚快钱的穷学生。）"
    mc "（扣掉交通费，一天能赚3000左右。干两周，就能攒够那块Boss DD-8的钱。）"
    mc "（为了它......我可以忍受任何脏活累活。我深吸一口气，走进了校园。）"
    scene black with Dissolve(1.5)
    play sound "audio/story/run1.ogg" loop volume 0.8
    mc "（我穿过校门，沿着指示牌前进。）"
    mc "（月之森的校园，确实大得离谱。欧式建筑、喷泉广场、修剪整齐的灌木......）"
    mc "（每一处都透着一股'花了很多钱'的气息。）"
    # 模拟环境音被刻意过滤，诡计开始运作
    stop sound fadeout 1.0
    play sound "audio/story/whispers_muffled.ogg" loop volume 0.6
    mc "（偶尔能看到结伴路过的女生。）"
    mc "（她们的步态依然优雅，但在目光触及到我的一瞬间，轻柔的交谈声却戛然而止。）"
    mc "（有人用手背或手帕微微掩住嘴唇，视线快速交汇，交换着某种克制却又难以掩饰的错愕。）"
    show text "{size=24}「那位是......」\n「怎么会是这副打扮......」\n「稍稍有些失礼了......」{/size}" at truecenter with dissolve
    pause 3.0
    hide text with dissolve
    mc "（距离其实很近，但我却听不清她们到底在说什么。那轻柔的声音就像被塞进水下过滤了一遍，只剩下嗡嗡的杂音。）"
    mc "（不过，也不难猜。）"
    mc "（大概是名门的大小姐们，在好奇我胸前这个廉价的工作证，或者是我这身和『上流社会』格格不入的打扮吧。）"
    mc "（但奇怪的是，她们的眼神里并没有我想象中那种高高在上的鄙夷。）"
    mc "（反而带着一种......莫名其妙的敬畏和小心翼翼的疏离。）"
    mc "（就好像，我是一个不该出现在这里的、异次元的投影。）"
    stop sound fadeout 2.0
    stop sound fadeout 2.0
    scene bg_school_courtyard with Dissolve(2.0)
    mc "（穿过教学楼区域，眼前出现了一片巨大的玫瑰中庭。）"
    mc "（修剪得过于完美，每一朵玫瑰都像是用尺子量过位置。红色、白色、粉色......在夕阳的映照下，美得有些不真实。）"
    mc "（就像......塑料做成的假花模型。这里的一切，都透着一股虚假的、布景般的气息。）"
    mc "（我加快脚步，穿过花园。）"
    mc "（越往里走，周围的人声就越少，那种像塑料一样的‘虚假感’就越弱。）"
    scene black with Dissolve(1.5)
    pause 2.0
    stop music fadeout 3.0
    mc "（建筑从现代化的教学楼，逐渐变成了老旧的红砖墙。尽头，是一道生锈的铁丝网。）"
    mc "（上面挂着斑驳的警示牌：『前方区域废弃·闲人免进』）"
    mc "（......闲人免进？那我这种拿钱办事的临时工，应该不算在内吧。）"
    mc "（我找了个破口，侧身翻了过去。）"
    mc "（翻过铁丝网的瞬间——世界......被切断了。）"
    mc "（刚才还是整洁的砖道和修剪过的草坪，现在脚下全是疯长的杂草和腐烂的落叶。）"
    mc "（空气突然变得粘稠潮湿，像有人把一块发霉的湿毛巾捂在了脸上。）"
    mc "（红砖小道消失了，取而代之的是疯长的爬山虎和被遗弃的建筑垃圾。）"
    mc "（生锈的铁架、破碎的花盆、发霉的木板......像是一个被时间彻底遗忘的角落。）"
    mc "（......）"
    mc "（我停下脚步，回头看了一眼。）"
    mc "（铁丝网后面，还能隐约看到玫瑰花园的光景。）"
    mc "（但那里......好像已经是另一个维度了。）"
    mc "（该不会真的有什么不对劲吧？......不，别自己吓自己。只是废弃区域而已，肯定很久没人打理了。）"
    stop sound fadeout 2.0
    scene bg_greenhouse_exterior with Dissolve(3.0)
    mc "（在杂草的尽头，出现了一座爬满藤蔓的玻璃建筑。）"
    mc "（旧第二温室——像一座被植物吞噬的巨大棺椁。）"
    mc "（玻璃穹顶布满裂纹与灰尘，夕阳的光透过来，被折射成病态的暗绿色。）"
    mc "（门是虚掩着的。生锈的铰链在风中发出刺耳的吱呀声，就像在警告外来者不要踏入。）"
    mc "（......算了，再吓人也只是个温室。我又不是来探险的，只要干完两周的活，拿到买效果器的钱就行了。）"
    mc "（我深吸一口气，推开了门。）"
    play sound "audio/story/rusty.ogg" volume 1.0
    stop sound fadeout 1.0
    scene bg_greenhouse_inside with Dissolve(2.5)
    play music story2 fadein 5.0 loop volume 0.6
    play sound "audio/story/water_drip.ogg" loop volume 0.4
    mc "（……稠密的死寂。）"
    mc "（踏进来的瞬间，外面的世界仿佛被彻底隔绝了。就连远处电车的声音，都一点也听不到了。）"
    mc "（只剩下远处某个破损的水管，在一滴一滴地漏水。）"
    mc "（潮湿的泥土味、发酵的腐叶土味、还有淡淡的霉味混杂在一起，让人有些喘不过气。）"
    mc "（光线从穹顶的裂缝洒下，形成一道道灰蒙蒙的光柱，像死去的聚光灯，照亮了空气中慢悠悠旋转的尘埃。）"
    mc "（像......时间的碎片。）"
    mc "（这......就是我要工作的地方？）"
    mc "（我咽了口唾沫。说实话，这糟糕的环境真让人有点后悔接下这份差事了。）"
    mc "（而且，这工作量......两周真的能清理完吗？）"
    mc "（正当我这么想的时候——）"
    mc "（等等。）"
    play sound "audio/story/shovel_digging_slow.ogg" loop volume 0.6
    "沙......"
    pause 1.0
    "沙......"
    mc "（那个声音，是什么时候开始的？）"
    # 镜头轻微推近，暗示视线的聚焦
    show bg_greenhouse_inside:
        linear 2.0 zoom 1.05 align (0.5, 0.5) 
    mc "（我猛地回过头。在生锈花架的最深处，不知何时，多了一个背影。）"
    show mu_blank at t11 with dissolve:
        zoom 0.8
        yoffset -80
    mc "（穿着月之森那标志性的深蓝制服。她正背对着我蹲在地上，手里拿着园艺小铲，给一株幼小的黄瓜苗松土。）"
    mc "（墨绿色的长发垂落在背后，随着手臂的动作微微晃动。）"
    "沙……沙……沙……"
    mc "（动作精准得可怕，每一次铲土的力度和角度都完全一致。简直就像一段设定好循环播放的程序。）"
    mc "（在这种长满霉菌的废墟里，她的制服却干净得一尘不染。）"
    mc "（这种强烈的违和感……简直就像是有人把一个精致的陶瓷人偶，遗忘在了垃圾堆里。）"
    mc "（......）"
    mc "（我应该......打个招呼吗？）"
    mc "（毕竟以后要在同一个空间工作。而且，她应该是这里的学生吧？为什么会一个人待在这种废弃温室里......）"
    mc "（算了，先礼貌地问候一下吧。）"
    mc "那个……不好意思打扰了。"
    pause 2.0
    mc "（......完全没有反应。）"
    mc "（她继续铲土，连肩膀的起伏都没有改变一下。）"
    mc "（......可能因为太专注，没听到？）"
    mc "（我清了清嗓子，朝她走近了两步，声音大了一点。）"
    mc "我是今天开始负责这里清理的兼职人员，名叫[persistent.playername]。"
    # 人格代码发生碰撞的瞬间
    hide mu_blank with dissolve
    show mu_blank_pause at t11 with dissolve
    stop sound # 铲土声戛然而止
    mc "（她的动作......停了。）"
    mc "（停了大概......三秒钟。）"
    mc "（在这三秒里，空气安静得让人耳鸣。我甚至觉得她会转过头来质问我。）"
    mc "（但是，没有。）"
    play sound "audio/story/shovel_digging_slow.ogg" loop volume 0.6
    "沙......沙......沙......"
    mc "（三秒后，铲土声重新响起。她没有回头，依然维持着那个机械的频率。）"
    mc "（......这是怎么回事？）"
    mc "（是听到了，但选择无视？）"
    mc "（不……不对。）"
    mc "（那种感觉，并不是‘出于傲慢的无视’。更像是一种物理层面上的‘无法识别’。）"
    mc "（就好像，在她的认知系统里，根本没有为了‘我’这个存在预留任何接收通道。）"
    mc "（在她的世界里，我发出的声音，大概和风声、水滴声，甚至温湿度计的刻度没有任何区别。）"
    mc "（彻底的……透明人待遇吗。）"
    mc "（......也好。反正我只是个拿钱办事的临时工。不产生交集，反而省去了麻烦。）"
    # 镜头拉回，视角转移
    show bg_greenhouse_inside:
        linear 1.5 zoom 1.0 align (0.5, 0.5)
    stop sound fadeout 2.0
    mc "（我耸耸肩，轻手轻脚地走向另一侧的工具架，尽量不去打扰这尊安静的人偶。）"
    mc "（拿钱办事，拿钱办事。她不理我，正好省事。）"
    hide mu_blank_pause with dissolve
    mc "（工具架上挂着生锈的铲子、扫帚、还有几个破旧的垃圾袋。看起来确实很久没人用了。）"
    mc "（我拿起扫帚，掂了掂重量。还能用。）"
    # --- 命运的触碰：吉他盒 ---
    mc "（正准备开始工作的时候——眼角余光，扫到了角落里的一个东西。）"
    mc "（嗯？）"
    show bg_greenhouse_corner_guitar as overlay at truecenter with dissolve:
        alpha 0.0
        linear 2.0 alpha 0.9
    pause 2.0
    mc "（在最阴暗的角落里，孤零零地躺着一个黑色的硬质琴盒。）"
    mc "（......吉他？）"
    mc "（我走近了一些。看这个形状......确实是电吉他的琴盒。）"
    mc "（虽然我不懂名牌包，但乐器我还是识货的。这个琴盒的做工和质感，绝对价格不菲。）"
    mc "（但是......上面落了极厚的一层灰。看这灰尘的厚度，至少一两个月没有被触碰过了。）"
    play sound "audio/story/heartbeat_single.ogg" volume 0.8
    with vpunch
    mc "（不知道为什么，看着那个被遗弃的琴盒，我的指尖没来由地抽动了一下。）"
    mc "（......）"
    mc "（......不过，这不关我的事。）"
    mc "（别多管闲事，[persistent.playername]。你的目标是时薪和Boss DD-8，不是名门大小姐的八卦。）"
    hide overlay with dissolve
    scene bg_greenhouse_inside
    mc "（我强行收回视线，拿起扫帚和垃圾袋，在这个沉默的兔穴里，开始了第一天的打工。）"
    play sound "audio/story/cleaning_debris.ogg" loop volume 0.5
    mc "（清理枯叶。整理花架。把破碎的花盆装进垃圾袋。）"
    mc "（很简单的工作。但......很安静。安静得让人感觉时间都被拉长了。）"
    mc "（唯一的声音，就是——那个女孩铲土的声音。）"
    play sound "audio/story/shovel_digging_slow.ogg" loop volume 0.4
    "沙......沙......沙......"
    mc "（她一直在那里。一动不动。就像这个温室长出来的一部分。）"
    mc "（泥土的味道更重了。像某种极其压抑的呼吸，从地底深处传来。让人......有点头晕。）"
    stop sound fadeout 2.0
    scene black with Dissolve(2.0)
    pause 1.0
    play music story3 fadein 4.0 loop volume 0.5
    mc "（不知不觉，原本透过玻璃的夕阳已经变成了暗淡的灰蓝色。）"
    mc "（温室里的光线逐渐被吞没。那些悬浮在半空的尘埃，在逆光中像燃尽的灰烬一样，缓慢下坠。）"
    
    scene bg_greenhouse_inside with Dissolve(2.5)
    
    show mu_blank at t11 with dissolve:
        zoom 0.8
        yoffset -80
        
    mc "（她依然维持着那个姿势。在这几个小时里，她像是和这片废墟彻底长在了一起。）"
    mc "（我看着她的侧脸轮廓……还有那头墨绿色的长发……）"
    
    # --- 叙事诡计：潜意识的既视感 ---
    play sound "audio/story/heartbeat_single.ogg" volume 0.5
    
    mc "（总感觉……非常熟悉。）"
    mc "（不是那种在电视上或者杂志上偶然瞥见的程度。而是一种……仿佛每天都能在镜子里看到的、刻在视网膜深处的熟悉感。）"
    mc "（但每当我试图在记忆里搜寻这张脸，大脑就像是触发了某种自我防御机制，传来一阵轻微的眩晕与刺痛。）"
    
    # 大脑立刻启动“补丁修正”
    mc "（......算了，大概是潜意识把她和哪个眼熟的明星搞混了吧。）"
    mc "（毕竟这种名门学校的学生，气质出众也很正常。）"
    
    mc "（但......那种如影随形的违和感，实在让人有些在意。）"
    mc "（我放下手里的扫帚，犹豫了一下。）"
    mc "（要不要......再试着说句话？）"
    mc "（虽然之前完全被当成了透明人......但至少，确认一下她是不是真的丧失了听觉功能？）"
    mc "（......试试吧。反正也不会有什么损失。）"
    mc "那个……"
    mc "虽然这话听起来有点蠢……不过，我们是不是在哪里见过？"
    stop music fadeout 2.0
    pause 2.0
    # 没有任何反应，只有风声
    play sound "audio/story/wind_draft.ogg" volume 0.6
    mc "（......）"
    mc "（回应我的，只有从破窗缝隙里钻进来的冷风。还有远处漏水管机械的滴水声。）"
    mc "（她......连眼睫毛都没颤动一下。）"
    mc "（......好吧。我认输。）"
    mc "（看来在她的世界里，我确实是一团没有任何质量的空气。）"
    hide mu_blank with dissolve
    show mu_blank_pause at t11 with dissolve
    mc "（就在我准备彻底放弃交流的时候——她动了。）"
    play music story4 fadein 2.0
    mc "（她缓缓站起身。因为蹲得太久，动作原本应该有些僵硬，但她却像上了发条的机械一样流畅。）"
    mc "（她没有看我一眼，甚至连停顿都没有，就这样径直走向了最阴暗的那个角落。）"
    mc "（走到那个落满灰尘的黑色琴盒旁边。）"
    mc "（她弯下腰，抱起了它。）"
    mc "（那个琴盒几乎有她大半个身子那么长。但她抱起它的动作却熟练得令人心惊，就像是……早就习惯了背负着这具沉重的遗骨。）"
    mc "（然后，她转过身，朝着门口走去。）"
    show mu_blank_pause:
        yalign 1.0   
        yoffset 0
        linear 1.5 xalign 1.5 alpha 0.0
    mc "啊，等——"
    # 音效：沉重的铁门关闭声
    play sound "audio/story/rusty_door_close.ogg"
    pause 1.0
    mc "（话还没说完，厚重的铁门就已经合上。）"
    mc "（连一秒钟的视线交汇都没有，她就这样背着那个巨大的枷锁，消失在了暮色里。）"
    mc "（真是个……不可理喻的家伙。）"
    mc "（明明有着那么强烈的存在感......但在她周围，却竖着一堵高耸入云的、拒绝与世界接触的高墙。）"
    mc "（把自己的心关在这样一个看不见的牢笼里......不觉得窒息吗？）"
    mc "（我苦笑着摇了摇头，看了一眼空荡荡、重归死寂的温室。）"
    mc "（刚才那铲土声回荡的地方，现在只剩下一株孤零零的黄瓜苗。）"
    mc "（还有......一个浅浅的、新翻过的土坑。证明她确实存在过。）"
    # --- 叙事诡计：意识进程的“休眠” ---
    mc "（......算了。今天的工时也凑够了，我也该回去了。）"
    scene black with Dissolve(2.0)
    stop music fadeout 3.0
    mc "（我锁上工具箱，推开温室的门。）"
    mc "（然而，就在我踏出那扇铁门的一瞬间——）"
    play sound "audio/story/white_noise_short.ogg" volume 0.3
    mc "（视线突然变得有些模糊。晚风吹得我有些睁不开眼。）"
    mc "（回家的记忆像融化在夜色里的水彩块，断断续续，怎么也拼凑不完整。）"
    mc "（大概……是第一天干体力活，太累了吧。）"
    mc "（那时的我还不知道。）"
    mc "（那个对自己、也对世界视而不见的女孩，到底背负着什么。）"
    mc "（我也根本不知道，自己在这个荒诞的舞台上，到底扮演着什么样的角色。）"
    mc "（我只是觉得——）"
    mc "（这份为了买效果器而接下的工作，大概会比想象中更让人喘不过气。）"
    pause 2.0
    # --- 第一天结束 ---
    scene black with Dissolve(3.0)
    window hide
    pause 1.5
    
    show text "{size=48}{font=fonts/cinematic.ttf}Day 1 - END{/font}{/size}" at truecenter with dissolve
    pause 2.5
    hide text with dissolve
    pause 1.0
    # 过渡提示
    show text "{size=32}接下来的日子\n\n沉默，将成为唯一的语言\n\n但在这片死寂的土壤之下——\n\n有什么东西，正在绝望地发酵{/size}" at truecenter with dissolve
    pause 5.0
    hide text with dissolve
    scene black with Dissolve(3.0)
    stop sound fadeout 3.0
    window hide
    pause 2.0
    jump sjdh


label prologue_part2:
    # --- 意识休眠与虚假记忆的过渡 ---
    scene black with dissolve
    stop music fadeout 3.0
    stop sound fadeout 2.0
    mc "（第一天结束后的回程，简直就像被按下了快进键。）"
    # 将“断片”完全归咎于体力透支，一气呵成，不留刻意思考的缝隙
    mc "（大概是因为平时太缺乏锻炼，第一天干这种高强度的体力活，身体直接累到了宕机。）"
    mc "（我只隐约记得自己浑浑噩噩地挤上了电车，等再回过神来的时候，人已经躺在出租屋的床上，连晚饭都没吃就直接睡死过去了。）"
    mc "（但在那种近乎断片的疲惫里，唯独有一个画面，在我的脑海里异常清晰。）"
    mc "（那个墨绿色长发的背影。还有那个落满灰尘的黑色琴盒。）"
    mc "（她到底是谁？总觉得……那种熟悉感挥之不去。）"
    mc "（......算了。）"
    mc "（那种名门大小姐，大概只是因为什么奇怪的理由偶尔去一次温室，今天刚好碰上而已。）"
    mc "（反正明天......应该不会再见到她了吧。）"
    mc "（......）"
    mc "（我是这么想的。）"
    # --- 到达温室 ---
    scene black with Dissolve(1.5)
    pause 1.0
    scene bg_greenhouse_exterior with Dissolve(2.0)
    play sound "audio/story/footsteps_gravel.ogg" loop volume 0.5
    
    mc "（穿过那片虚假的玫瑰中庭。）"
    mc "（翻过生锈的铁丝网。）"
    mc "（沿着爬山虎疯长的小径，旧第二温室再次出现在眼前。）"
    
    stop sound fadeout 1.0
    mc "（我深吸了一口气。推开门。）"
    
    play sound "audio/story/rusty.ogg"
    pause 1.5
    scene bg_greenhouse_inside with Dissolve(2.5)
    play music story2 fadein 4.0 loop volume 0.65
    
    mc "（然而——）"
    
    # 模拟人格进程载入
    play sound "audio/story/shovel_digging_slow.ogg" loop volume 0.6
    "沙……"
    pause 1.0
    "沙……" 
    show mu_blank at t11 with dissolve:
        zoom 0.8
        yoffset -80
    mc "（她还在那里。）"
    mc "（那个不可思议的女孩，像一株生了根的植物，蹲在昨天那个一模一样的位置。）"
    mc "（做着和昨天一模一样的动作。）"
    mc "（不仅如此……墨绿色的长发垂落的角度、甚至是校服裙摆折叠的阴影，都和昨天我的记忆分毫不差。）"
    mc "（简直就像……她这整个晚上根本没有离开过，一直被冻结在这个场景里一样。）"
    mc "（怎么可能。大概只是因为她的作息太规律，加上校服款式统一产生的错觉吧。）"
    mc "（我轻手轻脚地走进去，尽量不发出声音。）"
    pause 2.0
    stop sound fadeout 1.0
    mc "（毫无悬念，她连眼皮都没抬一下。）"
    mc "（依然把我过滤得干干净净。）"
    mc "（……早上好。）"
    mc "（我只在心里默默念了这句话，就自觉地闭上了嘴。）"
    play sound "audio/story/wind_draft.ogg" volume 0.5 
    
    mc "（破窗缝隙里钻进来的风，带着泥土发酵的腥味。）"
    mc "（除此之外，似乎还有一种奇怪的声音……像海潮一样，在极远的地方低鸣。）"
    mc "（那种声音很沉闷，带着一种让人溺水般的压抑感。）"
    
    # 大脑的强行解释
    mc "（这里明明是内陆的富人区，怎么会有海浪的声音？）"
    mc "（……大概是远处的电车驶过高架桥时，引发的空气共振吧。）"
    mc "（第一天打工太累，连听觉都开始出现幻觉了。）"
    mc "（我拿起扫帚，开始清理花架底下的枯叶。动作尽量放轻，像在避开一只随时会受惊的动物。）"
    mc "（这份工作极其枯燥，却也让人异常清醒。）"
    mc "（没有交流，没有音乐，只有她那恒定的铲土声，和我的呼吸声。）"
    mc "（也正因为如此，我开始注意到一些昨天没发现的细节。）"
    play sound "audio/story/shovel_digging_slow.ogg" loop volume 0.4
    "沙......沙......沙......"
    mc "（比如，她给那株黄瓜苗松土的节奏。）"
    mc "（很慢。慢到近乎一种极其谨慎的仪式。）"
    mc "（每一次铲土，都像是在拼命确认什么，又像是在……拖延什么。）"
    mc "（她偶尔会停下来，盯着那点刚冒头的绿芽看很久。）"
    mc "（十分钟。二十分钟。甚至半个小时。）"
    mc "（就那样一动不动，连呼吸的起伏都微不可察。像一尊被抽空了灵魂的白瓷人偶。）"
    mc "（……）"
    mc "（看着那株幼苗时，她的脑海里……到底在想什么呢？）"
    mc "（是在期待它开花结果吗？）"
    mc "（还是说……她只是单纯地需要一个‘可以名正言顺留在这个温室里发呆’的理由，来逃避外面的世界？）"
    mc "（不知道为什么，我竟然对一个连话都没说过的陌生人，产生了这么强烈的共情。）"
    mc "（就好像，那份难以言说的沉重和窒息，我自己也亲身体会过一样。）"
    mc "（……）"
    mc "（别乱猜了。[persistent.playername]。）"
    scene black with Dissolve(2.0)
    pause 1.0
    mc "（那一天，我们之间依然没有任何交流。）"
    mc "（她种地，我扫地。各自做着各自的事。）"
    mc "（就像两条平行线，被强行塞进同一个空间里，却永远不会相交。）"
    mc "（......但至少，我没有被解雇。）"
    mc "（这就够了。）"
    stop music fadeout 4.0
    stop sound fadeout 3.0
    play sound "audio/story/thunder_distant.ogg" volume 0.8
    pause 2.0
    play sound "audio/story/rain_heavy_loop.ogg" loop volume 0.9
    # 字幕：Day 3
    show text "{size=48}{font=fonts/cinematic.ttf}Day 3\n[ 浸透 ]{/font}{/size}" at truecenter with dissolve
    pause 2.5
    hide text with dissolve
    
    scene bg_greenhouse_inside_rain with Dissolve(3.0)
    play music "audio/story/zx02.ogg" fadein 5.0 loop volume 0.6
    mc "（第三天，秋雨来得毫无征兆。）"
    mc "（就像是这座城市突然陷入了某种无法排解的抑郁。早上出门时还是晴天，到了下午，天空就彻底黑了下来。）"
    mc "（我庆幸自己有个随时把折叠伞塞包里的习惯。虽然这把伞的骨架已经断了两根。）"
    mc "（我收起被雨水打湿的伞，狼狈地钻进温室。）"
    mc "呼……冷死了。"
    mc "（我搓着冻僵的手，跺了跺脚。试图把鞋底的泥蹭掉一些。）"
    mc "（明明刚才在路上跑的时候还出了一身汗，但踏进温室的瞬间，一股彻骨的寒意却从脚底窜了上来。）"
    mc "（这地方叫温室，可恒温系统早坏了。不仅毫无温度，甚至因为积攒的潮湿，比外面还要阴冷。）"
    mc "（雨水顺着穹顶的裂缝滴落。滴答......滴答......砸在地面上，溅起细小的水花。）"
    mc "（到处都在漏水。地面已经积了一层浅浅的水洼。）"
    mc "（我搓着手，习惯性地望向花架深处。）"
    
    show mu1_4 at t11 with dissolve:
        zoom 0.8
        yoffset -80
    mc "（她当然还在。）"
    mc "（但今天，她没有拿那把园艺铲。）"
    mc "（她站在靠近玻璃墙的位置，微微仰着头，看着雨水在污垢斑驳的穹顶上蜿蜒流下。）"
    mc "（灰蒙蒙的光线落在她的侧脸上，皮肤苍白得几乎有些透明。）"
    mc "（墨绿色的长发被湿气微微打卷，贴在颈侧。）"
    mc "（那个姿势......）"
    mc "（就好像......一只被剥夺了飞行能力的鸟，透过笼子的栅栏，注视着外面的天空。）"
    mc "（又或者……她根本不是在看雨，而是她自己就是这场雨的一部分。）"
    mc "（我没有打招呼。我已经学会了——在这个被遗弃的空间里，声音是多余的。）"
    mc "（我拿起抹布，走到离她五米远的另一侧，开始擦拭那些长满青苔的玻璃。）"
    play sound "audio/story/rain_on_glass.ogg" loop volume 0.8
    mc "（雨声很大。噼里啪啦，像无数细小的手指在敲击头顶的玻璃。）"
    mc "（这声音......成了天然的掩护。让我可以毫无顾忌地，在擦拭玻璃的间隙去观察她。）"
    mc "（她在看什么？雨痕？天空？还是......更远、更虚无的地方？）"
    mc "（她的瞳孔依然没有焦点。那双眼睛，就像深海里的盲鱼，望着无光的水面。）"
    mc "（空洞。迷茫。还有......一种仿佛透支了灵魂的疲惫。）"
    mc "（偶尔，她会轻轻动一下手指。像是想要去抓住玻璃上的某滴水，却又在半空停住。然后，无力地放下。）"
    mc "（就好像......连伸手的力气，或者说伸手的‘资格’，都已经被剥夺了。）"
    hide mu1_4 with dissolve
    pause 1.0
    show mu1_5 at t11 with dissolve:
        zoom 0.8
        yoffset -100
    mc "（突然，她伸出了手。）"
    mc "（那只修长、白皙，本该用来在聚光灯下弹奏吉他、或者翻阅精装书页的手。）"
    mc "（指尖轻轻贴上冰冷、满是污垢的玻璃。留下了一道短暂的雾痕。）"
    pause 2.0
    mu1 "......"
    # --- 叙事诡计：感官互通（Phantom Pain） ---
    play sound "audio/story/heartbeat_single.ogg" volume 0.8
    with vpunch
    mc "（极轻的叹息。几乎被巨大的雨声完全吞没。）"
    mc "（那声音里没有号啕的悲伤，也没有无聊的埋怨。更像是一种......长久的、已经把内部掏空的死寂。）"
    mc "（像植物在土中无声的枯萎，像石头在水底缓慢的风化。）"
    mc "（......）"
    mc "（为什么......）"
    mc "（只是看着那个背影，我的胸口突然像是被塞进了一团吸满水的海绵。）"
    mc "（连呼吸都变得酸涩、困难起来。）"
    mc "（......大概是因为温室里太闷了吧。加上这见鬼的下雨天。）"
    mc "（我对她产生的，绝对不是同情，更不是怜悯。而是一种......无法理解的错位感。）"
    mc "（她明明拥有一切我没有的东西：名校的制服，高不可攀的阶级，甚至连放在角落里的那个琴盒，都是我打几年工也买不起的奢侈品。）"
    mc "（可为什么......）"
    mc "（她看起来，却比我这个为了买一块Boss DD-8效果器就要拼命打零工的临时工——）"
    mc "（还要一无所有呢？）"
    mc "（......）"
    mc "（我强迫自己移开视线，用力擦拭着面前的玻璃。）"
    mc "（告诉自己，不要多想。这不关我的事，千万别和这个阶层的人扯上关系。）"
    mc "（......）"
    mc "（可是那个画面。）"
    mc "（她隔着雨水触碰玻璃的画面。）"
    mc "（却像某种无法擦除的水渍一样，死死地印在我的脑海里。挥之不去。）"
    scene black with Dissolve(2.5)
    stop music fadeout 4.0
    stop sound fadeout 4.0
    pause 2.0
    # --- Day 4 ---
    show text "{size=48}{font=fonts/cinematic.ttf}Day 4\n[ 涟漪 ]{/font}{/size}" at truecenter with dissolve
    pause 2.5
    hide text with dissolve
    scene bg_greenhouse_inside with Dissolve(2.0)
    play music story2 fadein 3.0 loop volume 0.6
    mc "（第四天。雨停了。）"
    mc "（温室顶棚积攒的雨水还在顺着裂缝滴落，地面湿漉漉的，反射着阴天灰暗的光。）"
    show mu1_4 at t11 with dissolve:
        zoom 0.8
        yoffset -80
    mc "（她又回到了那株黄瓜苗旁边。继续着那场慢节奏的、近乎自虐的仪式。）"
    play sound "audio/story/shovel_digging_slow.ogg" loop volume 0.6
    "沙......沙......沙......"
    mc "（我也继续着我的工作。清理、整理、擦拭。一切如常，沉默依旧。）"
    mc "（但不知道为什么……总觉得空气里的紧绷感消失了一点。取而代之的，是一种微妙的平衡。）"
    mc "（就像两个原本互相排斥的齿轮，开始习惯了彼此磨合时发出的微弱噪音。）"
    mc "（虽然还是不说话，但至少……那种让人窒息的‘透明感’，正在一点点消散。）"
    # --- Day 5: 临界点 (The Tipping Point) ---
    scene black with Dissolve(2.5)
    stop sound fadeout 3.0
    pause 2.0
    
    # 小岛式电影字卡
    show text "{size=48}{font=fonts/cinematic.ttf}Day 5\n[ 触碰 ]{/font}{/size}" at truecenter with dissolve
    pause 2.5
    hide text with dissolve
    scene bg_greenhouse_inside with Dissolve(3.0)
    show mu_blank at t11 with dissolve:
        zoom 0.8
        yoffset -80
        
    play music "audio/story/zx02.ogg" fadein 4.0 loop volume 0.65
    
    mc "（第五天。我已经完全适应了这个沉默的牢笼。）"
    mc "（现在的我，甚至能在这位不可思议的大小姐半径三米内无声通过。像影子，像幽灵，互不干扰，各安其所。）"
    
    mc "（......）"
    mc "（但有一件事，始终像根拔不掉的刺，扎在我的直觉里。）"
    
    # 特写吉他盒 (命运的焦点)
    show bg_greenhouse_corner_guitar as overlay at truecenter with dissolve:
        alpha 0.0
        linear 3.0 alpha 0.9
    pause 3.0
    
    mc "（那个黑色的硬质琴盒。它一直躺在那个阴暗的角落里，灰尘厚得能直接写字。）"
    mc "（我每天都会下意识地看它几眼。但我很清楚，我并非在好奇里面装的是什么昂贵的乐器。）"
    
    # 叙事诡计：技能本能的觉醒
    mc "（而是在意……她对待它的方式。）"
    mc "（在这种潮湿腐朽的环境里，木头会受潮，琴弦会生锈，琴颈会因为张力不均而弯曲。这简直是对乐器的慢性谋杀。）"
    mc "（明明每天都背过来，走时再背走，却绝对不去触碰。）"
    mc "（像是一株有毒的遗草，被她死死地种在心口最疼的地方。）"
    
    mc "（这到底是执念，还是某种自罚的逃避？）"
    mc "（那一刻，我盯着那个琴盒，脑海里竟然没来由地掠过一段凄凉的旋律。甚至……我的左手指尖，隐约能感觉到按压金属弦时的钝痛。）"
    
    hide overlay with dissolve
    
    # 冲突爆发：认知与感官的碰撞
    scene bg_greenhouse_inside
    
    # 使用图2风格的精细立绘（m3_0），展现墨缇斯人格觉醒前的压迫感
    show mu_blank at t11 with dissolve:
        zoom 1.0
        linear 1.5 zoom 1.3 yoffset 350 # 镜头急速拉近，表现心理上的压迫
        
    mc "（！！）"
    
    play sound "audio/story/heartbeat_single.ogg"
    with vpunch
    
    mc "（视线对上了。）"
    mc "（不知何时，她已经转过身，正直视着我。不……准确说，她是在盯着我注视的方向。）"
    
    mc "（在那双原本死水般的灰绿色眼睛里，此时正闪烁着一种近乎刺骨的光。）"
    mc "（像被触碰到逆鳞的野兽，带着一种极度脆弱的攻击性。）"
    
    mc "那、那个……我想着那上面灰挺厚的，可能对里面的东西不好……"
    mc "我想帮你擦一下。我保证，绝不会把它打开——"
    
    voice "audio/yuyin/mutsumi_no.ogg" # 这里可以用睦最冷、最干瘪的声音
    mu1 "……不用。"
    
    mc "（声音。那是她对我说的第一句话。轻得像要碎在风里，却冷得像结了冰的琴弦。）"
    
    pause 1.5
    
    mu1 "……那是，没关系的东西。"
    
    mc "（没关系的东西？）"
    mc "（我看在那双正在微微发抖的手。她指节泛白地攥着那把园艺小铲，身体紧绷得像是一根快要断裂的弦。）"
    mc "（既然真的没关系……为什么你的眼神，却像是要在下一秒钟崩溃一样？）"
    
    mc "（......）"
    mc "啊，明白了。我不碰，对不起。"
    
    # 墨缇斯的影子一闪而过 (伏笔)
    hide mu_blank with dissolve
    show mu_blank_pause at t11 with dissolve
    
    play sound "audio/story/shovel_digging_slow.ogg" loop volume 0.7
    
    mc "（她转回身。铲土声再次响起。空气里却多了一层随时会爆裂的电火花。）"
    mc "（我低下头，心跳快得几乎要撞碎肋骨。刚才那一瞬间，我看到的不是愤怒，而是恐惧。）"
    mc "（她在害怕……害怕这个‘没关系的东西’，会因为我的触碰而再次发出声音。）"
    
    stop sound fadeout 2.0
    
    mc "（我盯着表：17:55。还有五分钟就下班了。）"
    mc "（只要再搬完最后一袋腐叶土，就能结束这见鬼的一周，去乐器店试那块打折的效果器了。）"
    mc "（我是这么想的。如果，那时候……）"
    
    stop music fadeout 0.5
    
    # 灾难发生的瞬间 (镜头抖动)
    play sound "audio/story/fertilizer_spill.ogg"
    with hpunch
    
    mc "（如果我没有因为心急，而踩到那一滩还没干透的雨水——）"
    
    scene black with Dissolve(1.5)
    
    mc "（我就不会在倒下的瞬间，为了稳住身体，而死死地抓住了那个琴盒。）"
    
    play sound "audio/story/guitar_case_falling.ogg"
    with vpunch
    
    # 终极Meta伏笔：琴盒落地，发出了“砰”的一声。
    # 对于睦来说，这不仅仅是东西落地，而是她封闭的心被强行敲开。
    
    pause 2.0
    
    # 结束提示 (WA2式的情感拉扯感)
    show text "{size=48}{font=fonts/cinematic.ttf}Part 2 - END{/font}{/size}" at truecenter with dissolve
    pause 2.5
    hide text with dissolve
    
    show text "{size=32}第一周的沉默，至此终结。\n\n被掩盖的伤口，即将在这个雨后的黄昏里——\n\n彻底撕裂。{/size}" at truecenter with dissolve
    pause 5.0
    hide text with dissolve
    
    jump sjdh

label prologue_part3:
    scene black with Dissolve(2.0)
    mc "（如果那时候。）"
    mc "（我没有因为心急而脚下一滑——）"
    pause 1.5
    mc "（......）"
    mc "（但人生没有如果。）"
    mc "（发生的事，就是发生了。又或者说……，‘决定’让它发生了。）"
    scene bg_greenhouse_corner_dusk with Dissolve(3.0)
    stop music fadeout 3.0
    play sound "audio/story/heartbeat_slow.ogg" loop volume 0.5
    play sound "audio/story/low_hum_drone.ogg" loop volume 0.3
    mc "（17:55。）"
    mc "（还有五分钟就下班了。）"
    mc "（只剩最后那一袋20kg的腐叶土了。）"
    mc "（搬上去，今天的工时就满了。就能去乐器店试那块打折的Boss效果器……）"
    mc "（想着这些，我的脚步不由得快了几分。）"
    mc "（太急了。我知道自己太急了。）"
    mc "（但我只想快点结束这一切，离开这个压抑得让人无法呼吸的地方。）"
    mc "（我走到墙角，弯下腰，抓住肥料袋的边缘。用力一扯。）"
    mc "（……好重。）"
    mc "（不知道为什么，这具身体今天感觉异常的轻飘飘，完全使不上力气。）"
    mc "（明明平时搬20kg的东西没这么困难的……简直就像是用着别人的骨架一样使不上劲。是最近劳累过度了吗.....？）"
    mc "嘿......咻。"
    # 音效：布料摩擦 + 脚步轻微打滑
    play sound "audio/story/fabric_rustle.ogg"
    pause 0.5
    play sound "audio/story/footstep_slip.ogg"
    mc "（地面上还残留着没干透的雨水。）"
    mc "（或者......只是这具身体的肌肉已经到达了极限。）"
    mc "（重心猛地一偏。）"
    mc "（手指脱力，沉重的肥料袋脱手而出。）"
    window hide
    pause 0.8
    mc "！！"
    mc "（糟了——）"
    mc "（在那一瞬间，时间仿佛被大脑按下了极端的慢放键。）"
    mc "（我清晰地看到袋子在半空中翻转。看到它下坠的轨迹。看到它的落点——）"
    # 特写吉他盒
    show bg_greenhouse_corner_guitar as overlay at truecenter with dissolve:
        alpha 0.0
        linear 3.0 alpha 0.9
    pause 1.0
    
    mc "（是那个黑色的琴盒。）"
    mc "（不——）"
    mc "（这个重量和高度砸下去，里面的琴颈铁定会断裂，琴身会粉碎！）"
    mc "（那绝对是我赔不起的天文数字……！）"
    mc "危险——！！"
    # 惊悚音效切入，系统开始强行捏造CG
    play sound "audio/story/shock_sting_high.ogg" volume 1.2
    
    # 屏幕剧烈震动，模拟人格强行夺取身体控制权造成的“认知撕裂”
    with hpunch
    with vpunch
    mc "（那一瞬间。我的视网膜里，发生了一件完全违背物理常识的事。）"
    mc "（那个整整一周都像枯萎植物般一动不动、仿佛对世界失去所有反应的瓷娃娃……）"
    mc "（在袋子坠落的0.2秒内——消失了。）"
    scene white with Dissolve(0.1)
    scene black with Dissolve(0.1)
    mc "（不，不是消失。）"
    mc "（是......移动了。）"
    mc "（但那个速度，那种诡异的姿势……根本不像是人类依靠双腿走过去的。）"
    mc "（简直就像是画面掉帧了一样，前一秒还在三米外，下一秒，她就已经扑在了那个琴盒上！）"
    
    # 音效：肉体重重撞击地面 + 肥料袋闷响
    play sound "audio/story/heavy_bag_impact.ogg" volume 0.9
    play sound "audio/story/body_fall_thud.ogg" volume 1.0
    
    "砰！！！"
    "咚——"
    
    pause 1.2
    
    # 切回场景，诡计高潮：感官重叠 (Phantom Pain)
    scene bg_greenhouse_corner_dusk with Dissolve(1.0)
    
    mc "......呜！"
    
    play sound "audio/story/heartbeat_single.ogg" volume 1.0
    with vpunch
    mc "（痛。）"
    mc "（我因为惯性摔倒在地，手掌撑在粗糙的水泥地上，磨破了皮。掌心传来火辣辣的刺痛。）"
    mc "（但是……等等。）"
    mc "（为什么……我的后背和肩膀，也会传来一阵仿佛骨骼裂开般的剧痛？！）"
    
    mc "（明明被那袋20kg肥料砸中的，是扑在琴盒上的她才对啊！）"
    mc "（为什么……我感觉自己的肺里的空气都被那一击给挤了出去，连呼吸都带着血腥味？）"
    
    mc "（大脑像是要裂开一样轰鸣着。我顾不上这诡异的感官错乱，猛地抬起头，看向琴盒的位置。）"
    label prologue_part3_cont:
    # CG暗示或特写立绘：睦蜷缩护住琴盒，身上满是泥土
    show cg_mu_protect_guitar as cg at truecenter with Dissolve(2.0):
        alpha 0.0
        linear 2.0 alpha 1.0
        
    mc "......哈？"
    
    mc "（大脑有那么一瞬间的彻底空白。）"
    mc "（那个月之森的不可思议女孩......现在正侧躺在泥泞的地面上。）"
    mc "（20kg的肥料袋，重重地压在她的背上。那个重量和加速度......换做普通女生，足以压断肋骨，足以让人窒息。）"
    
    mc "（但她......她的双臂，却像死去的藤蔓死死缠住最后的支柱一样——）"
    mc "（将那个黑色的琴盒死死护在怀里。用自己的背，挡住了所有的冲击。）"
    mc "（琴盒——毫发无损。）"
    mc "（这......这是什么情况？）"
    
    # 叙事诡计：肉体伤害的共享与大脑的强制合理化
    play sound "audio/story/heartbeat_single.ogg" volume 0.8
    mc "（后背依然残留着极其诡异的钝痛。我手忙脚乱地试图从地上爬起来，膝盖刚一用力，就传来一阵钻心的刺痛。）"
    mc "（大概是我刚才滑倒时，膝盖重重磕在水泥地上了吧。）"
    mc "（但我根本顾不上自己，踉跄着冲过去，想先把那个致命的重物挪开。）"
    mc "你在干什么啊！会骨折的！快让我——"
    mu1 "……哈……哈……"
    mc "（她在喘息。急促、不稳、像是个溺水的人在徒劳地吞咽空气。）"
    mc "（但她没有试图推开背上的重量。）"
    mc "（她只是剧烈地颤抖着，将沾满泥污的脸颊，死死贴在琴盒冰冷的表面上。像在确认......它是否还有呼吸。）"
    mc "喂！没事吧？！让我看看伤口——"
    mc "（我伸出手，想去拉她的肩膀。）"
    mc "（但指尖还没碰到她沾满泥水的制服——）"
    stop sound fadeout 0.5
    # BGM切入：扭曲的八音盒变奏（Ave Mujica式冷峻与破碎感）
    play music story7 fadein 3.0 volume 0.6
    mu1 "别碰！！！"
    with vpunch
    with hpunch
    mc "！！"
    mc "（我僵在原地。）"
    mc "（那声音......带着一种濒临崩溃的惊惶。）"
    mc "（不是愤怒。不是斥责。）"
    mc "（而是纯粹的、本能的——求生。）"
    mc "（像一株被连根拔起的植物，在狂风中发出的最后一声哀鸣。）"
    # 立绘切换：浑身泥污，眼神惊恐
    hide cg with dissolve
    show mu1_6 at center with Dissolve(1.5):
        zoom 1.0
        linear 1.0 zoom 1.15
    mc "（她用力推开背上的肥料袋。袋子滚落时，溅起的泥水打在我的脸上，冰冷刺骨。）"
    mc "（那身原本一尘不染的深蓝校服，现在满是污渍。泥土、水渍、还有......血。）"
    mc "（她的膝盖破了。血丝顺着中筒袜缓缓渗下，在灰白色的布料上，绽开了一朵刺眼的暗红色花朵。）"
    # 叙事诡计：同步的痛觉
    play sound "audio/story/heartbeat_single.ogg" volume 0.6
    mc "（看着那道流血的伤口，我自己的膝盖竟然也跟着传来一阵火辣辣的幻痛。这该死的同理心简直敏锐得让人作呕。）"
    mc "（但她......连看都没看自己的伤口一眼。）"
    mc "（她的手指，死死扣住琴盒的把手。指节泛白，像是要把金属嵌进骨头里。）"
    mu1 "......不能碰......"
    mc "（声音在发抖。牙齿在打颤。连带着整个瘦弱的肩膀都在剧烈起伏。）"
    mu1 "......如果这个坏了......"
    mc "（她抬起头。第一次。真正意义上的第一次——直视着我。）"
    mc "（那双眼睛，我永远不会忘记。）"
    mc "（那根本不是一个活人的眼神。那是......一个快要淹死的人，死死盯着怀里最后一个氧气瓶的眼神。）"
    mu1 "如果坏了......"
    mu1 "我就真的......没有理由......"
    mu1 "......待在『那里』了......"
    mc "（『那里』......？）"
    mc "（那是哪里？家？学校？社团？还是......？）"
    mc "（但现在根本不是探究这个的时候——）"
    mc "喂，你的腿在流血！伤口很深，至少让我去叫医——"
    mu1 "......不用。"
    # 她强行站起，身体晃动
    show mu1_6:  
        linear 0.5 yalign 0.2
        linear 0.5 yalign 0.0

    mc "（她咬着牙，摇摇晃晃地站了起来。一把抱起那个几乎比她上半身还大的沉重琴盒。）"
    mc "（然后，像逃离一场足以将她吞噬的洪水一样，踉跄着冲向门口。）"
    show mu1_6 at center:
        easeout 1.2 xalign 1.5
        
    mc "等一下——！"
    hide mu1_6
    
    # 铁门剧烈开关 (现实中，是这具受了伤的身体逃离了现场)
    play sound "audio/story/rusty_door_close.ogg" volume 1.1
    scene bg_greenhouse_inside_dusk with Dissolve(2.0)
    stop sound fadeout 2.0
    
    mc "......"
    mc "（沉重的铁门砸上。温室重归死寂。）"
    mc "（只剩下滴水声、风声、还有我自己急促到几乎失控的呼吸。）"
    mc "（......）"
    mc "（我呆站在原地。看着地上散落的腐叶土。看着那一小滩......混合着泥水、正在逐渐晕开的暗红血迹。）"
    mc "（证明刚才的一切，不是幻觉，不是梦。是血淋淋的真实。）"
    mc "（我的脑子里，反复回放着她昨天的那句话。）"
    mc "『那是......没关系的东西。』"
    mc "（......骗子。）"
    
    mc "（刚才那个眼神。那根本不是在保护一把普通的乐器。）"
    mc "（那是在......护住自己仅存的灵魂。）"
    mc "（像一株被连根拔起的植物，死死抓住最后一缕带血的土壤。）"
    
    mc "（如果失去了那个琴盒，失去了那份沉重的枷锁。）"
    mc "（她大概就......）"
    mc "（......真的会死吧。）"
    # BGM渐强，压抑感加深
    play music story8 fadein 4.0 volume 0.7 loop
    mc "（我低头看着地上那滩混着腐叶的血迹。）"
    mc "（突然感到一阵刺骨的寒意，顺着脊椎一点点爬上来。）"
    mc "（不是因为温室漏风的温度。而是因为......）"
    mc "（......我意识到了。）"
    mc "（我这个只是想赚点外快的临时工，为了买一块效果器就跑到这种鬼地方来的底层人员......）"
    mc "（好像，窥见了一道绝对不该触碰的深渊。）"
    
    mc "（......）"
    mc "（等等。）"
    mc "（刚才......）"
    mc "（刚才她抬起头，像溺水者一样惊恐地看向我的那一瞬间。）"
    # 记忆闪回
    stop music fadeout 0.5
    play sound "audio/story/flashback_shock.ogg"
    scene white with Dissolve(0.1)
    pause 0.3
    scene bg_greenhouse_corner_dusk with Dissolve(1.5)
    mc "（那张脸。沾满泥污，因为恐惧而苍白，因为绝望而扭曲。）"
    mc "（那张脸......终于和记忆深处，那层一直隔着磨砂玻璃的熟悉感——）"
    mc "（重叠了。）"
    mc "（难怪......）"
    mc "（难怪我觉得这双眼睛如此熟悉。）"
    mc "（我见过她。）"
    mc "（不......）"
    mc "（应该说——）"
    mc "（全日本的人。）"
    mc "（大概都见过那张脸的轮廓。）"
    stop sound fadeout 2.0
    play music story9 fadein 3.0 volume 0.6
    mc "（那是......）"
    mc "（每周末黄金档综艺里。）"
    mc "（那个总是挂着标志性笑容。）"
    mc "（逗得全场捧腹大笑的男人——）"
    mc "（搞笑艺人，若叶隆文。）"
    mc "（那是......）"
    mc "（曾经在经典剧集《爱情码头》里。）"
    mc "（站在雨中哭得梨花带雨。）"
    mc "（让无数人心碎的国民女演员——）"
    mc "（森美奈美。）"
    mc "（那两个......）"
    mc "（站在演艺圈顶端的人。）"
    mc "（那对所有人都羡慕的模范夫妻。）"
    mc "（他们的影子。）"
    mc "（完美地融合在了......）"
    mc "（刚才那个少女的脸上。）"
    mc "（......）"
    mc "（从小到大铺天盖地的广告轰炸，想记不住都难。）"
    mc "（我早该想到的。）"
    mc "（我早就应该想到。）"
    mc "（她是那个备受瞩目的星二代。）"
    mc "（她是那个从小就被聚光灯照耀的孩子。）"
    mc "（她是......）"
    mc "（......）"
    mc "（但是......为什么？）"
    mc "（为什么那样的大小姐。）"
    mc "（会像个流浪猫一样，躲在这个废弃的温室里？）"
    mc "（为什么她的手上全是茧子？）"
    mc "（为什么她对世界如此冷漠？）"
    mc "（为什么她会为了一把吉他。）"
    mc "（露出那种......）"
    mc "（......仿佛世界末日般的表情？）"
    mc "（电视上的光鲜亮丽，和眼前这个流着血、跌跌撞撞逃跑的背影。）"
    mc "（这种巨大的认知撕裂感，让我的大脑产生了一阵强烈的眩晕。仿佛有什么东西要在脑壳里炸开一样。）"
    mc "（现在看来......）"
    mc "（我好像......）"
    mc "（真的窥见了绝对不该触碰的深渊。）"
    mc "（那个女孩的名字......）"
    mc "（若叶睦。）"
    scene black with Dissolve(3.0)
    stop music fadeout 4.0
    pause 2.0
    # 内心独白
    mc "（那一天。）"
    mc "（我惹上了，极其致命的麻烦。）"
    pause 2.0
    show text "{size=48}{font=fonts/yuwei.ttf}Part 3 - END{/font}{/size}" at truecenter with dissolve
    pause 2.5
    hide text with dissolve
    pause 1.5
    # 过渡到Part 4
    show text "{size=32}那一夜\n\n我在脑海里\n反复回放着那个场景\n\n那双充满恐惧的眼睛\n那句破碎的话语\n\n『如果坏了......』{/size}" at truecenter with dissolve
    pause 5.0
    hide text with dissolve
    pause 1.5
    # 跳转到Part 4
    jump sjdh


label prologue_part4:
    scene bg_greenhouse_corner_dusk with Dissolve(2.0)
    stop music fadeout 3.0
    play sound "audio/story/wind_draft.ogg" loop volume 0.6
    
    mc "…………"
    mc "（铁门撞击门框的沉重回音，在空荡荡的玻璃穹顶下回荡了很久，才终于消失。）"
    mc "（温室重新变回了那个巨大的、沉默的玻璃棺椁。）"
    
    mc "走了……吗。"
    
    mc "（我依然保持着伸出手想要拉住她的姿势，僵在半空中。）"
    mc "（指尖触碰到的，只有混合着土腥味的冷空气。）"
    
    mc "（太快了。从肥料袋滑落，到那个踉跄逃离的背影，一切发生得就像一场荒诞的快进电影。）"
    
    mc "嘶……"
    mc "（肾上腺素褪去后，痛觉开始迟钝地爬上神经。）"
    mc "（我低头看了看自己的手掌。刚才滑倒时下意识地撑在粗糙的水泥地上，掌心蹭掉了一层皮，渗出了细密的血珠。）"
    mc "（但这点痛，和刚才那一幕比起来，根本不算什么。）"
    
    menu:
        "（现在的我，应该……）"
        
        "追出去看看情况":
            $ mental_state = "worried"
            mc "（如果不去看看的话……那个伤口还在流血吧？）"
            mc "（我快步冲到门口，用力推开那扇沉重的铁门。）"
            
            scene bg_school_courtyard with vpunch
            mc "喂！若叶同学——！"
            
            mc "（.......空无一人。）"
            mc "（只有夕阳把铁丝网的影子拉得老长，像某种黑色的栅栏。）"
            mc "（也是……她是这所学校的大小姐，出了这扇门，自然有属于她的广阔世界，或者是某个我这种临时工进不去的高级休息室。）"
            mc "（我追上去又能做什么？递给她一张皱巴巴的创可贴吗？）"
            
            mc "……可恶。"
            scene bg_greenhouse_corner_dusk with Dissolve(1.5)
            mc "（我只能颓然地退回温室。）"
            
        "留在原地清理现场":
            $ mental_state = "calm"
            mc "（追上去又能怎么样？）"
            mc "（对她说“对不起我手滑了”？还是“你的伤口还好吗”？）"
            mc "（她刚才那个眼神……那种甚至带着恨意的恐惧。现在的我靠近她，只会让她更害怕吧。）"
            mc "（而且……如果不处理好这里的烂摊子，明天我就真的要因为失职被开除了。）"
            mc "（这才是成年人——或者说穷打工仔——该做的理性判断。）"
            mc "（虽然这么想，心里却像吞了铅块一样沉重。）"
            
    play music story6 fadein 4.0 volume 0.6 loop
    
    mc "（我转过身，面对着这一地狼藉。）"
    mc "（简直就像是灾难现场。那袋罪魁祸首的腐叶土横尸在路中间，袋口裂开，黑色的土撒得到处都是。）"
    
    mc "（还有……那个角落。）"
    
    mc "（水泥地上，几滴暗红色的液体异常刺眼。是血。）"
    mc "（刚才她为了护住琴盒，膝盖重重地磕在了这里。哪怕隔着制服和长袜，依然流了这么多血……）"
    
    mc "……真的假的啊。"
    mc "（我看向旁边。原本应该在那里的黑色琴盒已经不见了。）"
    mc "（那个落满了灰尘、被她像垃圾一样扔在角落的东西，在危险来临的那一刻，却比她自己的肉体更重要。）"
    
    mc "呼……"
    mc "（多想无益。干活吧。）"
    
    play sound "audio/story/heavy_bag_drag.ogg"
    mc "（我吃力地把那袋沉重的肥料袋扶起来，拖到墙角。）"
    
    play sound "audio/story/cleaning_debris.ogg" loop
    mc "（拿起扫帚，机械地把地上的泥土聚拢。）"
    mc "（沙——沙——）"
    mc "（这声音和她平时铲土的声音有点像。只不过，她是想让东西生长，而我是在掩埋刚才发生的“事故”。）"
    
    stop sound fadeout 1.0
    
    mc "（扫帚停在了那几滴血迹前。）"
    
    # 极度自然的“痛觉同调”掩盖
    mc "（我单膝跪下来，拿过抹布，用力在那块地面上擦拭。）"
    mc "（不知道是不是因为跪得太猛，我自己的膝盖也跟着传来一阵酸痛。）"
    mc "（水渍混着血迹，变成了一团污浊的淡粉色，最后彻底消失在灰色的水泥纹理中。）"
    
    mc "（差不多了。地面恢复了整洁，只要把角落里的枯叶铲走……）"
    
    play sound "audio/story/clink_metal.ogg" volume 1.0
    
    mc "嗯？"
    mc "（扫帚尖端传来了硬物碰撞的触感。声音很清脆，不像是碎石。）"
    mc "（我弯下腰，拨开那堆被扫到墙角的混合着泥水的枯叶。）"
    
    show item_old_keycard at truecenter with dissolve:
        yoffset 50
        zoom 1.2
    
    mc "这是……一张卡？"
    mc "（一张边缘已经泛黄、甚至有些开裂的磁卡。静静地躺在泥地里。）"
    mc "（奇怪……虽然边缘有磨损，但这卡片的表面却异常干净，没有沾上刚才撒落的泥土，甚至握在手里还有点温热的错觉。）"
    
    # 大脑完美的“逻辑自洽（补丁）”
    mc "（不过想想也正常。这张卡掉落的位置，刚好是这五天来她一直放吉他盒的地方。）"
    mc "（那个巨大的琴盒，一直像墓碑一样严丝合缝地压在这张卡片上，完美地隔绝了灰尘和刚才的泥水吧。）"
    
    window show
    "{color=#aaa}【月之森女子学园 · 设施管理部】{/color}"
    "{color=#aaa}类型：通用门禁卡（Staff Only）{/color}"
    "{color=#aaa}编号：NO.009{/color}"
    "{color=#aaa}状态：{color=#f00}已挂失/作废{/color}{/color}"
    window hide
    
    mc "（早已作废的旧版员工卡？）"
    mc "（看这个磨损程度，应该是以前负责这里的人不小心弄丢，被琴盒压住才一直没被发现吧。）"
    
    menu:
        "扔进垃圾桶":
            mc "（反正已经作废了，留着也没用。我正准备把它扔进垃圾袋，手指却突然停住了。）"
            mc "（等等。这里的门锁……好像就是那种几十年前的老式磁力锁。）"
            mc "（现在的智能校园卡刷不开，但我手里的这张老古董……说不定反而能用？）"
            mc "（鬼使神差地，我把它收了回来。）"
            
        "偷偷收起来":
            mc "（我有种奇怪的直觉。）"
            mc "（这个温室，对于若叶睦来说，绝对不仅仅是个发呆的地方。）"
            mc "（如果以后发生了什么事……我是说如果。这张能绕过正规门禁的通用卡，说不定能派上用场。）"
            mc "（就当是刚才被吓出一身冷汗的“精神补偿”吧。）"
    
    hide item_old_keycard with dissolve
    
    mc "（卡片带着一丝温润的凉意，滑进了我的口袋。）"
    mc "（它和我的那张临时工牌碰在一起，发出了轻微的咔哒声。）"
    mc "呼……"
    mc "（环顾四周。）"
    mc "（原本充满生活气息（虽然只有一点点）的角落，现在空荡荡的。）"
    mc "（没有了那个沉默的背影。）"
    mc "（没有了那个压抑的琴盒。）"
    mc "（这里变回了一个普通的、废弃的破烂温室。）"
    mc "（但我知道，有什么东西已经变了。）"
    mc "（那个眼神。）"
    mc "（那个拼死也要守护某样东西的眼神。）"
    mc "（像一根刺，扎进了我这个只想混日子的打工仔心里。）"
    mc "若叶……睦。"
    mc "（我咀嚼着这个名字。）"
    mc "（回家吧。）"
    
    stop music fadeout 5.0
    scene black with Dissolve(3.0)
    
    scene black with Dissolve(3.0)
    stop music fadeout 4.0
    stop sound fadeout 3.0
    
    # 字幕
    show text "{size=48}{font=fonts/yuwei.ttf}Day 5 - 18:30{/font}{/size}" at truecenter with dissolve
    pause 2.5
    hide text with dissolve
    
    # --- 场景1: 回家的电车上 ---
    scene bg_train_interior_night with Dissolve(2.5)
    play sound "audio/story/train_pass.ogg" loop volume 0.6
    play music story6 fadein 4.0 loop volume 0.5
    
    mc "（我跌坐在座位上，身体像是一滩烂泥，深深地陷进异常柔软的椅背里。）"
    mc "（太累了。）"
    mc "（从精神到肉体的双重透支，剥夺了我对周围一切的感知。我甚至连睁开眼睛的力气都没有。）"
    
    # 诡计：极其自然的客观描述，完全不提“这是异常”
    mc "（封闭的空间里很安静。没有晚高峰的嘈杂，只剩下平稳低沉的引擎声，以及空气中若有若无的、让人昏昏欲睡的白茶香气。）"
    mc "（手掌上擦破的皮已经结痂了，但那种刺痛感......好像还残留在神经末梢。）"
    # 闪回效果
    scene white with Dissolve(0.1)
    pause 0.2
    scene bg_greenhouse_corner_dusk with Dissolve(0.3)
    show cg_mu_protect_guitar at center with dissolve:
        zoom 1.15
        alpha 0.7
    mu0 "如果坏了......我就真的......"
    mu0 "......没有理由......待在『那里』了......"
    scene bg_train_interior_night with Dissolve(0.5)
    with vpunch
    
    mc "（......）"
    mc "（她那时候的眼神。那不是在保护什么名贵的乐器。那是......溺水的人死死抱住最后一根浮木的眼神。）"
    # 电车报站
    "『下一站——涩谷。Shibuya.』"
    mc "（我按了下车铃,机械地站起身。）"
    mc "（周围的乘客面无表情地滑动手机。）"
    mc "（没人会在意一个浑身泥土味的高中生在想什么。）"
    stop sound fadeout 2.0
    stop music fadeout 2.0
    # --- 场景2: 深夜的出租屋 ---，1.25 14:08 后面的内容因为音效原因还没开搞
    scene black with Dissolve(2.0)
    pause 1.0
    scene bg_apartment_room with Dissolve(2.5)
    pause 1.0
    mc "（回到家。我连灯都没开，直接把包甩在了地上。）"
    mc "（包落地时发出了一声发闷的钝响。我拖着像灌了铅一样的双腿，在黑暗中走向书桌。）"
    mc "（平时只要走两步就能跨过去的六叠房间，今天走起来，竟觉得这段路被疲惫拉得格外漫长。）"
    mc "（为了每个月的房租，我每周都得去那个压抑的温室打工。）"
    # 拿出工资单道具
    show item_payslip at truecenter with dissolve:
        zoom 1.2
    pause 2.0
    mc "（我从口袋里掏出这周的临时工资单。）"
    mc "（纸张的触感很厚实，边缘甚至有些割手。借着窗外透进来的微弱路灯，我扫了一眼上面打印的文字。）"
    mc "『月之森女子学园·环境维护临时人员——本周工时:15小时,税前16,500日元』"
    mc "（扣掉税和交通费,到手大概14,000。再干三周,就能攒够那块Boss DD-8的钱了。）"
    hide item_payslip with dissolve
    mc "（......应该是这样的。）"
    mc "（应该。）"
    # 坐到电脑前
    play sound "audio/story/chair_pull.ogg"
    pause 0.5
    mc "（我打开笔记本电脑,屏幕的冷光照亮了昏暗的房间。）"
    mc "（本来想直接洗澡睡觉。）"
    mc "（但手指不受控制地在搜索栏里敲下了那个名字。）"
    play sound "audio/story/keyboard_typing.ogg" volume 0.7
    pause 2.0
    play sound "audio/story/mouse_click.ogg"
    pause 0.5
    play music "audio/mortis/7 普通与平静.ogg" fadein 3.0 loop volume 0.55
    mc "『若叶睦』"
    pause 1.5
    mc "（搜索结果瞬间跳了出来。）"
    mc "（维基百科、娱乐新闻、粉丝博客......）"
    mc "（全都是关于那对『国民模范夫妻』的女儿。）"
    show text "{size=32}若叶睦\n父:若叶隆文(搞笑艺人)\n母:森美奈美(演员)\n现就读:月之森女子学园高等部一年级{/size}" at truecenter with dissolve
    pause 4.0
    hide text with dissolve
    mc "（点开图片搜索。）"
    play sound "audio/story/mouse_click.ogg"
    pause 1.0
    mc "（屏幕上出现了无数张照片。）"
    mc "（颁奖典礼上,她穿着昂贵的礼服,站在父母身边,露出得体的微笑。）"
    mc "（慈善活动的合影里,她举着捐款牌,眼神温柔。）"
    mc "（杂志访谈的截图:『若叶家的掌上明珠——继承双亲才华的优等生』）"
    mc "（......这就是月之森的不可思议女孩？）"
    mc "（我盯着屏幕上那张完美无瑕的脸。）"
    mc "（精致的妆容。专业的表情管理。）"
    mc "（就像......）"
    mc "（就像温室里那个抱着琴盒颤抖的人,和这些照片里的她......）"
    mc "（根本不是同一个物种。）"
    mc "（我继续往下翻。）"
    mc "（然后......看到了一条三个月前的娱乐新闻。）"
    show text "{size=28}『若叶隆文长女睦突然休学!?\n事务所回应:因健康原因暂时休养』{/size}" at truecenter with dissolve
    pause 3.5
    hide text with dissolve
    mc "（健康原因......）"
    mc "（我想起了她手上的茧子。）"
    mc "（想起了她每天机械地给黄瓜松土的样子。）"
    mc "（还有那双空洞的、像深海鱼一样的眼睛。）"
    mc "（这叫健康原因？）"
    mc "（骗鬼呢。）"
    # 点开评论区
    play sound "audio/story/mouse_click.ogg"
    pause 1.0
    mc "（评论区里全是猜测。）"
    show text "{size=24}「肯定是压力太大了吧,星二代也不容易」\n「听说月之森的升学竞争很恐怖」\n「该不会是霸凌吧......」\n「真不愧是森美奈美的女儿」{/size}" at truecenter with dissolve
    pause 5.0
    hide text with dissolve
    mc "（我关掉了网页。）"
    play sound "audio/story/mouse_click.ogg"
    scene bg_apartment_room with Dissolve(1.5)
    mc "（电脑屏幕暗下去,房间重新陷入昏暗。）"
    mc "（只有窗外偶尔经过的车灯,在墙上投下短暂的光影。）"
    mc "（不知道什么时候,外面开始下雨了。）"
    mc "（雨水打在窗户上,发出细碎的声响。）"
    mc "（我躺在床上,盯着天花板上斑驳的水渍。）"
    

    mc "（若叶睦。）"
    mc "（一个拥有我永远无法企及的一切——名门学校、富裕家庭、甚至被媒体铺好的光明未来的人。）"
    
    mc "（可为什么......）"
    mc "（为什么她看起来，比我这个为了下个月房租发愁、甚至要为了买一块打折效果器拼命的临时工......还要一无所有？）"
    
    mc "（那把吉他。）"
    mc "（她说『如果坏了,就没有理由待在那里了』。）"
    mc "（『那里』到底是哪里？家？学校？还是......某个她不得不去扮演完美人偶的冰冷舞台？）"
    mc "（而那把落满灰尘的吉他，就是她的『入场券』。）"
    mc "（一张一旦破损，就会被立刻驱逐出场的、极其悲哀的门票。）"
    
    mc "（......该死。）"
    mc "（我翻了个身，用力揉了揉眉心。我为什么要想这些？）"
    mc "（我只是个拿钱办事的底层打工人。她那种阶层的人生，和我根本就不在同一个宇宙里。）"
    
    # 手机震动 (现实中是睦的智能机，主角感知为自己的旧手机)
    play sound "audio/story/phone_vibrate.ogg" volume 0.8
    pause 1.0
    play sound "audio/story/phone_vibrate.ogg" volume 0.8
    pause 0.5
    
    mc "（床头的手机连续震了两下。我闭着眼睛摸索过去。）"
    
    # 隐性诡计：触感与重量的错位
    mc "（冰冷的金属外壳压在掌心，今天拿在手里，总觉得沉甸甸的，坠得手腕发酸。）"
    mc "（我强撑开一条眼缝，看了一眼屏幕。）"
    
    # 显示邮件通知
    show text "{size=32}发件人:月之森女子学园总务处\n主题:关于旧校舍维护工作的进度通知{/size}" at truecenter with dissolve
    pause 3.0
    hide text with dissolve
    
    mc "（......）"
    mc "（心脏猛地一紧，困意瞬间消散了大半。）"
    mc "（不会吧......该不会是因为今天发生的‘事故’，或者是那个女孩告了状，我直接被解雇了吧？）"
    
    # 打开邮件
    play sound "audio/story/mouse_click.ogg"
    pause 1.5
    
    show text "{size=26}尊敬的临时工作人员:\n\n感谢您本周的辛勤工作。\n因旧第二温室设施维护进度调整,\n下周工作时间将延长至每次4小时。\n时薪不变,请按原定时间到岗。\n\n——月之森女子学园总务处{/size}" at truecenter with dissolve
    pause 6.0
    hide text with dissolve
    
    mc "（......不是解雇通知。）"
    mc "（只是工时调整。算下来，工资反而变多了。）"
    
    mc "（我长长地吐出一口气。）"
    mc "（也就是说......）"
    mc "（下周,我还得回到那个温室。）"
    mc "（还得面对那个像受伤野兽一样的少女。）"
    
    
    mc "（雨下得更大了。）"
    mc "（我把手机扔到一边,翻了个身。）"
    mc "（可能是因为今天真的已经累到了极点，平时那张硬邦邦的单人床，此刻睡起来竟然像是一团毫无阻力的云，整个人都在无限地往下陷。）"
    mc "（......算了。反正我也没有选择的余地。）"
    mc "（为了那块效果器，为了下个月的房租......我还得继续去那个地方。）"
    mc "（就算那里埋着什么绝对不该触碰的深渊。）"
    mc "（就算那个女孩最后看向我的眼神，像极了某种正在缓慢窒息的东西。）"
    mc "（......）"
    mc "（我闭上眼睛。）"
    scene black with Dissolve(4.0)
    stop music fadeout 5.0
    stop sound fadeout 4.0
    mc "（在半梦半醒之间，我感觉自己的左手手指，正在无意识地抽动。）"
    mc "（紧接着，我仿佛听到了一阵声音。不是雨声，也不是电车的轰鸣。）"
    mc "（而是......一阵极其冰冷、精准、几乎没有任何多余感情的吉他扫弦声。）"
    play sound "audio/story/guitar_cold_strum.ogg" volume 0.6
    pause 2.0
    
    mc "（它就在我的脑海深处，在那个寂静的玻璃温室里，孤独地回响。）"
    
    pause 2.0
    pause 2.0
    
    # 转场字幕
    show text "{size=40}{font=fonts/yuwei.ttf}那一夜\n我做了一个梦\n\n梦见一座被藤蔓吞噬的玻璃棺材\n和一个抱着吉他\n无法逃离的人偶{/font}{/size}" at truecenter with dissolve
    pause 5.0
    hide text with dissolve
    
    pause 2.0
    
    scene black with Dissolve(3.0)
    show text "{size=48}{font=fonts/yuwei.ttf}Part 4 - END{/font}{/size}" at truecenter with dissolve
    pause 2.5
    hide text with dissolve
    pause 1.5
    
    stop music fadeout 3.0
    stop sound fadeout 2.0

    jump sjdh

label prologue_part5:
    scene black with Dissolve(3.0)
    stop music fadeout 4.0
    stop sound fadeout 3.0
    
    # 周一字幕
    show text "{size=48}{font=fonts/cinematic.ttf}Day 8\n[ 惯性 ]{/font}{/size}" at truecenter with dissolve
    pause 2.5
    hide text with dissolve
    
    # --- 场景1: 犹豫的早晨 ---
    scene bg_apartment_room with Dissolve(2.5)
    play music "audio/bgm/morning_unease.ogg" fadein 4.0 loop volume 0.5
    play sound "audio/story/alarm_clock.ogg"
    
    mc "（早上六点。床头的闹钟准时响起。）"
    mc "（声音听起来比平时还要沉闷，像是在水下敲击玻璃的回音。我伸出沉重的手臂，凭着肌肉记忆精准地按掉了它。）"
    
    stop sound fadeout 1.0
    
    mc "（我睁开眼，盯着天花板上那片极其繁复的、像暗花图腾一样的‘水渍’发呆。）"
    
    mc "（周一了。）"
    mc "（距离温室里那场狼狈的‘事故’，已经过去了整整两天。）"
    mc "（周末的这四十八小时里，我几乎没有踏出过房门半步。那天摔倒留下的后遗症比想象中严重，背部和膝盖的酸痛感像潮水一样，反反复复地折磨着我的神经。）"
    
    mc "（我本来以为自己早就下定了决心。理智非常清晰地告诉我，应该立刻辞职。）"
    mc "（那个长满爬山虎的温室，还有那个把自己锁在深渊里的女孩，都透着一股绝对不能靠近的危险气息。）"
    
    mc "（但每次我打开手机邮箱，敲好辞职信的抬头时——）"
    mc "（手指却像是不受控制一样，怎么也按不下那个发送键。）"
    
    # 闪回睦受伤的画面
    scene white with Dissolve(0.2)
    scene bg_greenhouse_corner_dusk with Dissolve(0.5)
    show mu1_uniform_dirty_scared at center with dissolve:
        zoom 1.15
        alpha 0.6
    
    mu0 "如果坏了......我就真的......"
    mu0 "......没有理由......待在『那里』了......"
    
    scene bg_apartment_room with Dissolve(1.0)
    
    play sound "audio/story/heartbeat_single.ogg" volume 0.7
    
    mc "（一闭上眼睛，那双满是泥污和绝望的眼睛就会浮现在黑暗里。）"
    mc "（像一个正在缓慢溺水的人，死死抱住怀里最后一块即将碎裂的浮木。）"
    mc "（伴随着那个画面，我的胸口就会涌起一股近乎物理意义上的窒息感，压得我喘不过气来。）"
    
    mc "（......该死。）"
    mc "（我用力抓了抓头发，把那些乱七八糟的思绪强行赶出大脑。）"
    mc "（我为什么要在意这种事？我只是个拿时薪的临时工，拿钱办事，按时走人。她的人生、她的痛苦，和我这个为了房租发愁的人有什么关系？）"
    
    mc "（......）"
    mc "（在心里这么警告了自己无数遍后，我还是掀开被子，从床上爬了起来。）"
    
    # 起床准备
    play sound "audio/story/clothes_rustle.ogg"
    pause 1.5
    play sound "audio/story/water_splash.ogg"
    pause 1.0
    
    mc "（卫生间里。我捧起冷水狠狠拍了拍脸，试图让自己清醒一点。）"
    mc "（我抬起头，看向洗手台上方那面边缘有些模糊的镜子。）"
    # 终极叙事诡计：镜子里的“盲点” (特征过滤)
    mc "（镜子里的人眼眶微红，眼底带着明显的乌青。因为周末几乎没怎么睡，脸色苍白得像一张纸。）"
    mc "（缺乏血色的嘴唇，加上毫无生气的眼神......完完全全就是一副被生活榨干了的、疲惫不堪的底层社畜模样。）"
    mc "（看着这副倒霉的德行，我自嘲地扯了扯嘴角，移开了视线。）"
    mc "（算了。）"
    mc "（反正再干两周，就能攒够买那块Boss DD-8效果器的钱了。）"
    mc "（等把效果器买到手，我就立刻辞职，再也不踏进那个见鬼的学校半步。）"
    mc "（就当是为了时薪......再忍耐一下吧。）"
    
    # --- 场景2: 前往温室的路上 ---
    scene black with Dissolve(2.0)
    pause 1.0
    
    scene bg_train_interior_afternoon with Dissolve(2.5)
    play sound "audio/story/train_running.ogg" loop volume 0.6
    play music "audio/bgm/fragile_connection.ogg" fadein 4.0 loop volume 0.55
    
    mc "（下午四点的电车，依然拥挤。）"
    mc "（我站在门边，看着窗外倒退的风景。）"
    mc "（涩谷的高楼大厦逐渐被低矮的住宅区取代。）"
    mc "（然后是成片的绿地和围墙。）"
    
    mc "（月之森女子学园——光听名字，就像是童话里才会存在的地方。）"
    mc "（但实际上，只要是人聚集的地方，就永远免不了阴暗的角落。表面越是光鲜亮丽，内里藏着的溃烂就越是难以见光。）"
    
    mc "（就像......那个名叫若叶睦的女孩。）"
    
    mc "（昨晚在网上查到的资料，像一团乱麻一样塞在我的脑子里。）"
    mc "（搞笑艺人若叶隆文的女儿。国民女演员森美奈美的掌上明珠。从小就在聚光灯和长枪短炮下长大的、毫无瑕疵的完美结晶。）"
    
    mc "（新闻照片里的她，总是笑得那么得体。站在光鲜亮丽的父母身边，像个被精心打理过的、昂贵的瓷器装饰品。）"
    
    mc "（但温室里的她——）"
    mc "（那双空洞的、没有焦点的眼睛。那副面对任何事都仿佛彻底死心的表情。）"
    mc "（到底经历了怎样的崩坏，才会让一个人从照片里那个鲜活的女孩，变成一具被抽掉了灵魂的人偶？）"
    
    # 隐性诡计升级：吉他手的肌肉记忆冲突
    mc "（嘶......）"
    mc "（我无意识地搓了搓左手。指尖传来一阵熟悉的、被钢弦勒进肉里的发麻感。）"
    
    # 大脑直接生成了虚假记忆，将Mutsumi/Mortis的弹奏归结为自己的练习
    mc "（肯定是周末在出租屋里，抱着那把破电吉他练得太猛了。）"
    mc "（连食指和小指现在都还在神经质地微微抽动，仿佛肌肉里还残留着那种极其沉重、甚至带着点狂躁的扫弦节奏。）"
    
    mc "（不过说起来……我周末到底具体弹了些什么？弹了多久？）"
    mc "（记忆简直像是一团浆糊，脑子里只剩下那种连床都下不来的极度疲惫感。）"
    
    # 极其自然的打工人式吐槽，毫无痕迹地缝合逻辑Bug
    mc "（大概是因为太渴望早点买到那块Boss DD-8效果器，搞得我走火入魔，连做梦都在疯狂推弦吧。）"
    mc "（真够好笑的，身体都已经累得要散架了，手指倒是一刻也不肯停。等拿到这笔工资，绝对要好好睡个三天三夜。）"
    
    stop sound fadeout 2.0
    play sound "audio/story/train_stop.ogg"
    
    "『月之森站到了，请乘客注意安全。』"
    
    mc "（我下了车。）"
    
    # --- 场景3: 学园入口的观察 ---
    scene bg_school_gate_afternoon with Dissolve(2.5)
    play sound "audio/story/school_bell_distant.ogg"
    pause 2.0
    
    mc "（校门口，穿着深蓝制服的女学生们三三两两地走出来。）"
    mc "（她们用那种克制而优雅的音量谈笑着，手里拿着补习班的资料或是社团的用具。阳光洒在她们身上，一切都显得那么正常且美好。）"
    
    mc "（但在这些正常的人群里——）"
    mc "（我并没有看到那抹令人窒息的墨绿色长发。）"
    
    mc "（也是。）"
    mc "（像她那种把自己完全封闭起来、拒绝与世界接触的人，这个时间，大概早就躲进那个只有她一个人的温室里了吧。）"
    
    play sound "audio/story/footsteps_gravel.ogg" loop volume 0.6
    
    mc "（我熟练地穿过玫瑰中庭。那些修剪完美的假花依然让人感到不适。）"
    mc "（翻过铁丝网，踩着杂草丛生的小径，一步步靠近旧第二温室。）"
    
    mc "（越是靠近那扇生锈的铁门，我的心跳就越是控制不住地加快。）"
    
    mc "（今天……她会是什么反应？）"
    mc "（是会像往常一样，把我当成一团透明的空气？）"
    mc "（还是会像上周五那样，用那种防备、恐惧的眼神死死盯着我？）"
    
    stop sound fadeout 1.0
    
    mc "（我停在门前，深吸了一口气。肺里灌满了属于这里的、潮湿发霉的空气。）"
    mc "（我把手放在冰冷的门把手上。）"
    
    mc "（推开了门。）"
    
    play sound "audio/story/rusty_door_open.ogg"
    scene bg_greenhouse_inside with Dissolve(2.5)
    play music "audio/bgm/dusk_greenhouse.ogg" fadein 5.0 loop volume 0.6
    
    mc "（吱呀——）"
    mc "（沉重的铁门发出熟悉的呻吟声。）"
    
    mc "（温室内部依然是那副半废墟的死寂模样。灰尘在从穹顶裂缝射入的光线里缓慢飞舞，空气中弥漫着泥土、发酵的腐叶、还有某种冷冰冰的潮湿气味。）"
    
    # 听到铲土声
    play sound "audio/story/shovel_digging_slow.ogg" loop volume 0.5
    
    mc "（......）"
    mc "（那个声音。）"
    
    "沙......沙......沙......"
    
    mc "（她在。）"
    
    pause 2.0
    
    show mu1_4 at t11 with dissolve:
        zoom 0.8
        yoffset -80
    
    mc "（月之森的不可思议女孩。依然蹲在那里。）"
    
    mc "（和上周五我离开时一模一样的位置。和上周一模一样的姿势。）"
    mc "（墨绿色的长发垂落下来，遮住了大半个侧脸。校服裙摆的褶皱，甚至连投在地上的阴影角度都没什么变化。）"
    
    mc "（仿佛......时间在这个角落里是绝对静止的。）"
    mc "（仿佛上周五那场伴随着鲜血和惊恐的'事故'，只是我大梦一场的幻觉。）"
    
    mc "（她还在种那株黄瓜。机械地、专注地、一下一下地松土。像一台只剩下最后一条运行指令的精密机器。）"
    
    mc "（......）"
    
    mc "（我松了一口气，轻手轻脚地走向另一侧的工具架。）"
    mc "（尽量不发出任何多余的声音。就像我在过去一周里学会的那样——乖乖成为这个密闭空间里的一团透明空气。）"
    
    play sound "audio/story/footsteps_careful.ogg"
    pause 2.0
    stop sound fadeout 1.0
    
    mc "（我拿起扫帚，开始今天的工作。清理杂草、整理废弃的花架、把角落的枯叶装进垃圾袋......这些活我已经做得很熟练了。）"
    
    mc "（今天的她，依然对我没有任何反应。就像上周一到周四那样，完美地把我当成了温室设施的一部分。）"
    mc "（自动洒水器、温湿度计、还有......一把会自己移动的扫帚。）"
    
    mc "（......这样也好。至少不用面对搭话被无视的尴尬。）"
    
    # --- 场景5: 工作中的观察 ---
    scene black with Dissolve(2.0)
    pause 1.0
    
    show text "{size=40}{font=fonts/cinematic.ttf}一小时后{/font}{/size}" at truecenter with dissolve
    pause 2.0
    hide text with dissolve
    
    scene bg_greenhouse_inside with Dissolve(2.0)
    play sound "audio/story/broom_sweep.ogg" loop volume 0.5
    
    mc "（我在清理温室角落的杂物。）"
    mc "（生锈的铁丝架、破碎的陶瓷花盆、发霉的园艺手套、还有一些不知道是什么年代的肥料袋......）"
    mc "（月之森这种名门学校，自然不缺钱去建新的现代化设施。所以这些旧的东西，就这样被理所当然地扔在一边，任其在阴暗处慢慢腐烂。）"
    
    mc "（......这和某些人的命运，倒是讽刺地相似。）"
    
    stop sound fadeout 1.5
    
    show mu_blank at t11 with dissolve:
        zoom 0.8
        yoffset -80
    
    mc "（而在几米外，若叶睦还在照料她的黄瓜苗。）"
    mc "（那株幼苗已经长到了小腿高。嫩绿的叶片在昏暗的光线里，显得格外鲜活，和周围死气沉沉的环境形成了极其强烈的割裂感。）"
    
    play sound "audio/story/watering_can.ogg"
    pause 2.0
    
    mc "（她拿起旁边的小洒水壶。动作小心翼翼，像是在对待某种极其易碎的宝物。）"
    mc "（水流细细地浇在根部，一滴都没有溅到外面的泥土上。）"
    
    stop sound fadeout 1.0
    
    mc "（那种专注......真的很奇怪。）"
    mc "（明明只是一株普通的黄瓜。种在这种恒温系统彻底坏掉的废弃温室里，连能不能熬过这个秋天都是个问题。）"
    mc "（但她却......像在照顾一个新生的婴儿一样。不，甚至比那更小心、更绝望。）"
    
    mc "（我停下扫地的动作，隔着几米的距离，忍不住多看了几眼。）"
    
    mc "（我的视线落在了她的手上。）"
    mc "（那是一双修长、苍白，本该是用来在聚光灯下弹奏斯坦威钢琴，或者端着红茶杯的手。）"
    mc "（但在她左手的虎口处，却有一层明显的厚茧。四根手指的指尖上，也布满了深浅不一的老茧和勒痕。）"
    
    # 细节呼应：用共同的痛觉产生羁绊
    mc "（我下意识地用大拇指摩挲了一下自己左手的指尖。）"
    mc "（我知道那不是种地留下的痕迹。因为那和我自己指尖上，为了练吉他而留下的硬茧几乎一模一样。）"
    
    mc "（那是一双属于演奏者的手。一双属于音乐家的手。）"
    
    mc "（......）"
    mc "（我不自觉地将视线移向了角落的那个黑色琴盒。）"
    
    show bg_greenhouse_corner_guitar as overlay at truecenter with dissolve:
        alpha 0.0
        linear 2.0 alpha 0.7
    pause 2.5
    
    mc "（今天，它依然静静地躺在那里。）"
    mc "（但上面的灰尘已经被彻底擦干净了——大概是上周五我离开后，她自己一点一点擦掉的吧。）"
    mc "（失去灰尘的掩盖，琴盒表面露出了几道细微的、新的擦痕。看起来......她确实比谁都爱惜这个东西。）"
    
    mc "（但是——她从来不打开它。）"
    
    hide overlay with dissolve
    show mu_blank at t11:
        zoom 0.8
        yoffset -80
    
    mc "（每天都带来。每天都背走。却从始至终，都不肯碰一下里面的琴。）"
    
    mc "（这种极度矛盾的行为......）"
    mc "（简直就像是一个快要窒息的人把氧气瓶背在身上，却拼命捂住自己的口鼻拒绝呼吸一样。）"
    mc "（明明需要，却又恐惧。明明渴望，却又逃避。）"
    
    mc "（......她到底在害怕什么？里面装的难道不是吉他，而是某种吃人的怪物吗？）"
    
    mc "（我越想越觉得胸口发闷。这种死寂的沉默，这种把自己彻底隔绝在世界之外的状态——绝对不是一个正常人该有的。）"
    mc "（如果继续这样下去......她迟早有一天会彻底崩溃的吧。）"
    
    mc "（......）"
    
    mc "（不对，这和我有什么关系？我只是个临时工。名门大小姐的精神状态，轮不到我一个穷学生来操心。）"
    
    mc "（......）"
    mc "（......但是。）"
    
    mc "（如果我今天什么都不做，就这么冷眼旁观下去——）"
    mc "（总觉得......我一定会后悔。）"
    
    # 主角决定尝试交流
    mc "（......试试看吧。至少......让她知道，这个像坟墓一样的温室里，不是只有她一个人在喘气。）"
    
    mc "（但是......要说什么？）"
    mc "（她明显不是那种会回应天气或者闲聊的人。随便搭话，大概率会再次收获长达十分钟的死寂。）"
    
    mc "（需要一个......她可能会感兴趣，或者至少不会让她立刻产生应激反应的话题。）"
    
    mc "（植物？吉他？还是......）"
    
    # 关键选择点 - 决定结局走向
    menu:
        mc "（......）"
        
        "「那株黄瓜，长得挺好的。」":
            $ route_safe = True
            $ mu_affection = 5
            
            mc "那个......若叶同学。"
            
            pause 2.0
            
            mc "（完全没有反应。）"
            mc "（她连肩膀的弧度都没变一下，继续专注地铲土。）"
            
            play sound "audio/story/shovel_digging_slow.ogg" loop volume 0.4
            "沙......沙......沙......"
            
            mc "（......果然。）"
            mc "（我就知道会是这种空气人待遇。）"
            mc "（但既然已经硬着头皮开口了，总不能在这个时候把话咽回去。）"
            
            mc "你种的那株黄瓜......长得挺好的。"
            
            stop sound fadeout 0.5
            pause 2.5
            
            mc "（铲土声，停了。）"
            
            hide mu1_4 with dissolve
            show mu1_3 at t11 with dissolve
            
            mc "（她的动作僵住了。然后，非常、非常缓慢地——）"
            mc "（侧过脸，用那双深灰色的眼睛看向我。）"
            
            mc "（那眼神里没有上周五那种刺骨的敌意，也没有被搭话的困惑。）"
            mc "（只有一种......难以名状的、仿佛电路短路般的茫然。）"
            mc "（就好像在她的世界里，从来没有人用这种毫无所求的、纯粹日常的语气和她搭过话。）"
            
            pause 3.0
            
            mu1 "......是吗。"
            
            mc "（声音极轻。轻得像是一片快要融化的雪花，几乎要被温室缝隙里的风声彻底吞没。）"
            mc "（但她确实......回应了。）"
            
            mc "嗯。比上周又长高了不少。再过一两周，应该就能结果了吧？"
            
            show mu1_0 at t11 with dissolve
            
            mu1 "......不知道。"
            mu1 "......我没种过。"
            
            mc "（说完这句话，她转回身，重新拿起了那把小铲子。）"
            mc "（对话就这样突兀地结束了。）"
            
            mc "（但至少......她回应了。）"
            mc "（虽然只有短短的两句话，虽然声音小得可怜，虽然听起来依然拒人于千里之外。）"
            mc "（但这就像是在一面绝对光滑的冰墙上，敲出了一道微不可察的裂缝。）"
            
            play sound "audio/story/shovel_digging_slow.ogg" loop volume 0.5
            
            mc "（我重新拿起扫帚。听着那恒定的沙沙声，心里莫名其妙地松了一口长气。）"
            
            jump part5_continue
            
        "「你是......森美奈美的女儿吗？」":
            $ route_bad = True
            $ bad_ending_triggered = True
            
            mc "那个......不好意思。"
            
            pause 2.0
            
            mc "（毫无悬念，完全没有反应。）"
            mc "（她继续铲土，仿佛我是这温室里的一粒灰尘。）"
            
            mc "（......算了，既然怎么搭话都会被无视，那干脆就直接点吧。）"
            
            mc "你是......森美奈美的女儿吗？"
            
            # 音效：铲土声戛然而止
            stop sound fadeout 0.1
            
            pause 3.0
            
            mc "（......）"
            mc "（铲土声，瞬间消失了。）"
            
            hide mu1_4 with dissolve
            show mu1_1 at t11 with dissolve:
                zoom 1.0
                linear 1.5 zoom 1.2
            
            mc "（她的身体彻底僵住了。就像是在极寒中被瞬间冻结的标本。）"
            
            mc "（然后——她缓缓转过头。）"
            
            mc "！"
            
            play sound "audio/story/heartbeat_single.ogg"
            with vpunch
            
            mc "（那双眼睛。）"
            mc "（我从未在任何一个活人身上，见过那种眼神。）"
            mc "（没有被揭穿身份的愤怒，也没有被冒犯的悲伤——）"
            mc "（而是一种......空洞到令人头皮发麻的冰冷。）"
            
            mc "（就像......在看一具正在腐烂的尸体。或者说，她觉得自己就是那具尸体。）"
            
            pause 2.5
            
            mu1 "......你也是。"
            
            mc "什、什么？"
            
            mu1 "......和其他人......一样。"
            
            mc "（她的声音，平静得可怕。没有一丝起伏，也没有一毫情感。）"
            mc "（就像是一台被拔掉电源前，最后播报了一句乱码的机器。）"
            
            mu1 "......我懂了。"
            
            hide mu1_1 with dissolve
            show mu1_0 at t11 with dissolve
            
            mc "（她站起身。动作机械而流畅。用那双修长的手，拍了拍裙摆上并不存在的灰尘。）"
            
            mc "等、等一下——"
            
            mu1 "......没关系。"
            mu1 "......我习惯了。"
            
            mc "（她走向最阴暗的角落，动作麻木地抱起那个黑色的琴盒。背在肩上。）"
            
            show mu1_0:
                linear 2.0 xalign 0.8
            
            mc "若叶同学，我不是那个意思！我只是在网上看到了新闻——"
            
            mu1 "......再见。"
            
            show mu1_0:
                linear 1.5 xalign 1.5 alpha 0.0
            
            play sound "audio/story/rusty_door_close.ogg" volume 1.2
            with hpunch
            
            pause 1.5
            
            scene bg_greenhouse_inside with dissolve
            
            mc "（沉重的铁门砸上。）"
            mc "（她走了。连最后半个眼神，都没有再施舍给我。）"
            
            mc "（......）"
            
            mc "（我做错什么了吗？）"
            mc "（我只是......好奇地确认一下身份而已啊......）"
            
            mc "（......）"
            
            mc "（温室重归死寂。只剩下我一个人，还有那株......她孤零零留下的黄瓜苗。）"
            mc "（在这个瞬间，我突然有种强烈的预感。）"
            mc "（那扇铁门......大概永远不会再为我打开了。）"
            
            # 跳转到坏结局
            jump prologue_bad_ending

label part5_continue:
    scene black with Dissolve(2.0)
    pause 1.0
    show text "{size=40}{font=fonts/cinematic.ttf}一小时后{/font}{/size}" at truecenter with dissolve
    pause 2.0
    hide text with dissolve
    
    scene bg_greenhouse_inside with Dissolve(2.0)
    play sound "audio/story/broom_sweep.ogg" loop volume 0.4
    
    mc "（之后的一个小时，我们又回到了彻底的沉默状态。）"
    mc "（她种地，我清理。偶尔，我会借着扫地的动作偷偷瞄她一眼。）"
    mc "（她依然面无表情，机械地重复着照料那株黄瓜的动作。）"
    
    mc "（但不知道为什么——总觉得空气里的压迫感没那么重了。）"
    mc "（至少，她不再把我当成一团完全透明的空气。我能感觉到，我的‘存在体积’，在这个温室里被稍微认可了一点点。）"
    
    stop sound fadeout 1.5
    mc "（这就算是......微小的进步吧。）"
    
    # 时间推移到黄昏
    scene black with Dissolve(2.0)
    pause 1.0
    
    scene bg_greenhouse_inside_dusk with Dissolve(2.5)
    play music "audio/bgm/turning_point.ogg" fadein 3.0 loop volume 0.55
    play sound "audio/story/sunset_wind.ogg" loop volume 0.5
    
    mc "（不知不觉，夕阳开始透过玻璃穹顶洒进来。整个废墟般的温室被染成了病态的暗红色，就像浸泡在发酵的葡萄酒里一样。）"
    mc "（我擦完最后一块玻璃，放下抹布。今天的工作，差不多该结束了。）"
    
    show mu_blank at t11 with dissolve:
        zoom 0.8
        yoffset -80
        
    mc "（她还在那里。蹲在那株黄瓜苗旁边。）"
    mc "（但这次，她没有在铲土。只是......静静地看着那株植物。一动不动。）"
    
    mc "（......）"
    mc "（我走向工具架，准备收拾东西下班。）"
    mc "（但刚走出两步——）"
    
    hide mu_blank with dissolve
    show mu_blank_pause at t11 with dissolve
    
    mu1 "......手。"
    
    mc "！"
    mc "（她.....她又主动说话了？）"
    
    mc "怎、怎么了？"
    
    pause 1.5
    
    mu1 "......有茧。"
    
    mc "（她没有看我的脸，而是盯着我垂在身侧的左手。）"
    
    mc "（我下意识地抬起左手。四根手指的指尖上，确实有着长期按压钢弦留下的厚茧。大概是因为周末在出租屋里练得太狠，现在还微微发红。）"
    
    mc "啊......嗯。我会弹一点吉他。业余水平而已，平时一个人在家里瞎弹的。"
    
    show mu_blank at t11 with dissolve
    
    mu1 "......这样。"
    
    mc "（她极轻地吐出两个字。然后，盯着我的指尖看了很久。那种眼神非常奇怪......就像是在看一面镜子里的自己。）"
    mc "（然后，她收回视线，重新陷入了沉默。）"
    
    mc "（......）"
    mc "（这算什么？确认同类？）"
    
    mc "（我想继续问她些什么。比如那个黑色的琴盒里装的是什么型号的琴，比如她是不是也弹吉他。）"
    mc "（但看她那副重新封闭起来的样子——大概就算问了，也只会被无视吧。）"
    
    mc "（算了。今天能交流到这个程度，对这座冰山来说已经是奇迹了。不能太贪心。）"
    
    mc "那个......我该走了。明天见。"
    
    pause 2.0
    
    mu1 "......嗯。"
    
    mc "（她极细微地点了点头。虽然依然没有表情，但至少......回应了。）"
    
    # --- 场景6: 极简的谢意与感官同调 ---
    mc "（我走向门口的工具架，准备放下扫帚。）"
    
    mc "（但在放扫帚的时候——我注意到了架子的边缘，放着一个小小的东西。）"
    
    mc "（我愣了一下，拿起来一看。）"
    
    mc "（是一枚崭新的、毫无花哨的普通创可贴。）"
    
    mc "（......）"
    mc "（我记得我刚才拿扫帚的时候，这里明明什么都没有的。）"
    
    mc "（我转过头看向温室深处。）"
    
    show mu_blank at t11 with dissolve
    
    mc "（她还保持着蹲在地上的姿势。背对着我，安静地看着那株黄瓜苗，仿佛完全沉浸在自己的世界里。）"
    
    mc "（......这家伙。）"
    mc "（明明连正眼都不愿意多看我一下。）"
    mc "（却趁着我背对她擦玻璃的时候，偷偷摸摸地把这种东西放在我一定要碰的工具架上吗。）"
    
    mc "（连一句只言片语的便签都没有。这种极度别扭、一声不吭的交流方式......还真是符合她的作风。）"
    
    # 隐性诡计的极致发挥：伤痛共享
    mc "（我无声地笑了笑，撕开包装，把创可贴仔细地贴在掌心早上不小心擦破的伤口处。）"
    
    play sound "audio/story/heartbeat_single.ogg" volume 0.5
    
    mc "（不知道是不是心理作用......）"
    mc "（就在创可贴贴好的那一瞬间。）"
    mc "（我突然觉得，连带着这几天一直隐隐作痛的膝盖，似乎都好受了不少。紧绷的神经也跟着奇妙地放松了下来。）"
    mc "（心理暗示的作用，还真是强大得离谱啊。）"
    
    mc "（......）"
    
    mc "（我最后看了一眼那个被夕阳拉长的背影。）"
    mc "（不知道为什么，我觉得......她似乎没有之前那么孤独了。）"
    
    # --- 场景7: 离开与序章收尾 ---
    play sound "audio/story/rusty_door_close.ogg"
    scene black with Dissolve(2.0)
    
    mc "（我离开了温室。）"
    mc "（穿过爬满爬山虎的小径。翻过生锈的铁丝网。回到那个修剪得过于完美的玫瑰花园。）"
    
    mc "（夕阳已经快落山了。天空被染成了深红色，像一场即将谢幕的沉重演出。）"
    
    mc "（今天......算是巨大的进展了吧。）"
    mc "（至少，她不再把我当成完全透明的了。至少，她会回应我的话了。）"
    
    scene bg_school_gate_dusk with Dissolve(2.5)
    play music "audio/bgm/evening_mystery.ogg" fadein 3.0 loop volume 0.5
    
    mc "（我独自一人，走出了校门。）"
    mc "（晚风吹过，带来了一丝属于秋天的寒意。）"
    
    mc "（我和她......能成为朋友吗？）"
    mc "（一个为了买吉他效果器拼命打工的穷学生，和一个把自己锁在废墟里的大小姐。）"
    mc "（怎么想，都是两条不该相交的平行线。）"
    
    mc "（算了，想这些没用。先回去吧。）"
    
    # 结尾独白
    scene black with Dissolve(3.0)
    stop music fadeout 4.0
    stop sound fadeout 3.0
    
    mc "（那一天。）"
    mc "（我还不知道。）"
    mc "（我，以及那个把自己锁在废墟里的女孩。）"
    mc "（我们之间那根极细极脆的线，究竟牵着什么。）"
    mc "（......）"
    mc "（我只是单纯地觉得——）"
    mc "（能和她说上话，已经是不小的进步了。）"
    mc "（但我不知道的是——）"
    mc "（这场属于『我们』的、荒诞又残酷的同调......）"
    mc "（才刚刚拉开序幕。）"
    
    pause 2.0
    
    # 神秘音效：远处传来极轻的吉他声 (肌肉记忆的神经回响)
    play sound "audio/story/guitar_harmonics_ghost.ogg" volume 0.3
    pause 4.0
    
    mc "（......嗯？）"
    mc "（刚才......好像听到了吉他的泛音？）"
    mc "（......）"
    mc "（......算了，大概是幻听吧。）"
    
    pause 2.0
    scene black with Dissolve(3.0)
    show text "{size=48}{font=fonts/cinematic.ttf}序章： Down the Rabbit Hole\n—— 土中之呼吸 (De Profundis) - END{/font}{/size}" at truecenter with dissolve
    pause 3.0
    hide text with dissolve
    pause 1.5
    
    jump sjdh

label prologue_bad_ending:
    scene black with Dissolve(3.0)
    pause 2.0
    # Day 9
    show text "{size=48}{font=fonts/yuwei.ttf}Day 9 (Tuesday){/font}{/size}" at truecenter with dissolve
    pause 2.5
    hide text with dissolve
    scene bg_greenhouse_inside with Dissolve(2.5)
    play music "audio/story/bad_ending.ogg" fadein 4.0 loop volume 0.5
    mc "（第二天，我照常来到温室。）"
    mc "（......昨天说了那句话之后，我就知道了。）"
    mc "（那句问她是不是森美奈美女儿的话，大概不该问的。）"
    mc "（但发生的事，就是发生了。）"
    mc "（但是——）"
    mc "（她不在。）"
    pause 2.0
    mc "（温室里空荡荡的。）"
    mc "（只剩下那株黄瓜苗，孤零零地立在那里。）"
    mc "（连同那个黑色的吉他琴盒，也一并消失得无影无踪。）"
    mc "（空气里那种紧绷的、活人呼吸的频率，被彻底抽干了。）"
    mc "（奇怪......今天的温室，好像比平时暗了很多。连从缝隙里漏进来的风，都感觉不到什么温度了。）"
    # 隐性诡计：感官开始降级
    mc "（......）"
    # Day 10
    scene black with Dissolve(2.0)
    show text "{size=48}{font=fonts/yuwei.ttf}Day 10 (Wednesday){/font}{/size}" at truecenter with dissolve
    pause 2.5
    hide text with dissolve
    scene bg_greenhouse_inside with Dissolve(2.0)
    mc "（第三天。）"
    mc "（她还是没来。）"
    mc "（黄瓜苗开始有些萎蔫了。）"
    mc "（大概是缺水。）"
    mc "（我犹豫了一下......）"
    mc "（还是拿起洒水壶，给它浇了点水。）"
    mc "（......）"
    # Day 11
    scene black with Dissolve(2.0)
    show text "{size=48}{font=fonts/yuwei.ttf}Day 11 (Thursday){/font}{/size}" at truecenter with dissolve
    pause 2.5
    hide text with dissolve
    scene bg_greenhouse_inside with Dissolve(2.0)
    mc "（第四天。）"
    mc "（还是没来。）"
    mc "（那株失去照料的黄瓜苗，已经开始无可挽回地萎蔫了。）"
    
    mc "（我拿起洒水壶，机械地给它浇水。但水珠顺着枯黄的叶片滑落，根本渗不进干裂的泥土里。）"
    mc "（就像我现在的状态一样。）"
    mc "（我开始后悔了。）"
    mc "（为什么......要提起森美奈美？）"
    mc "（为什么......要自作聪明地问那种问题？）"
    mc "（为什么非要亲手撕开那层脆弱的伪装？）"
    mc "（......）"
    play sound "audio/story/phone_vibrate.ogg"
    pause 1.0
    mc "（口袋里的手机传来极其微弱的震动。甚至连震感都变得有些模糊。）"
    mc "（是一封来自学校总务处的邮件。）"
    show text "{size=28}『通知：\n经评估，该区域已无继续投入维护之必要。\n旧第二温室的特别清理合同，\n将于本周五提前终止。\n您的门禁权限将同步收回。\n\n——月之森女子学园总务处』{/size}" at truecenter with dissolve    
    pause 8.0
    hide text with dissolve
    mc "（......）"
    mc "（评估结束。合同终止。）"
    mc "（这简直就像是在对我说：你存在的意义，已经没有了。）"
    scene black with Dissolve(2.0)
    show text "{size=48}{font=fonts/yuwei.ttf}Day 12 (Friday){/font}{/size}" at truecenter with dissolve
    pause 2.5
    hide text with dissolve
    scene bg_greenhouse_inside with Dissolve(2.5)
    mc "（最后一天。）"
    mc "（我收拾好工具，准备离开。）"
    mc "（黄瓜苗已经完全枯萎了。）"
    mc "（尽管我每天都给它浇水。）"
    mc "（但......没有她照料。）"
    mc "（它还是死了。）"
    mc "（......）"
    mc "（我蹲下身，看着那株干枯的植物。）"
    mc "（脑海里反复回放着她最后的那句话——）"
    mc "（『......你也是，和其他人一样。』）"
    mc "（......）"
    mc "（对不起。）"
    mc "（我不该......）"
    mc "（不该把你，和那个名字联系在一起。）"
    play sound "audio/story/rusty_door_close.ogg"
    scene black with Dissolve(3.0)
    stop music fadeout 5.0
    
    mc "（我慢慢站起身，推开温室的铁门。）"
    
    play sound "audio/story/rusty_door_close.ogg" volume 0.6
    
    mc "（咔哒。门锁死的声音。极其沉闷，仿佛隔着一层厚厚的海绵。）"
    
    mc "（不知为何，强烈的疲惫感突然像海啸一样吞没了我。连挪动双腿都变得异常困难。）"
    
    mc "（对了，下班之后，我原本打算去做什么来着？）"
    mc "（......哦，去乐器店，买那块Boss DD-8效果器。）"
    
    mc "（可是......）"
    mc "（那个效果器……是什么来着？）"
    mc "（我为什么……突然一点都想不起来它的声音了？）"
    
    scene black with Dissolve(4.0)
    
    mc "（视野越来越暗。）"
    mc "（回家的电车......是要坐哪一条线？）"
    mc "（我的出租屋......是在哪个方向？）"
    
    mc "（想不起来了。什么都想不起来了。）"
    mc "（不过......也无所谓了吧。）"
    
    mc "（真的......太累了。）"
    mc "（如果在这个时候闭上眼睛，应该会被原谅吧。）"
    show text "{size=40}{font=fonts/yuwei.ttf}BAD END\n\n『被遗忘的温室』\n\n你失去了\n接近她内心的机会\n\n温室里\n再也没有人来过{/font}{/size}" at truecenter with dissolve
    pause 10.0
    hide text with dissolve
    pause 2.0
    jump sjdh



    