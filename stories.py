"""Haymaker stories: the five premade stories, the Create-a-World options and every text that goes with them.

Put this file next to web_app.py.

HOW TO ADD THE CHARACTER PICTURES
  Upload one picture per card into the folder  assets/stories/  with EXACTLY these names (.jpg, .jpeg, .png or .webp):
      kade.jpg   shadow_prince.jpg   system.jpg   nova.jpg   titan.jpg
  A portrait picture about 800 x 1100 pixels works best. Keep each file under 300 KB (phones load them every visit).
  Until a picture exists the card shows its own colour gradient and emoji, so the page never looks empty.

HOW TO CHANGE A STORY
  Each entry in STORIES has a persona (who the narrator is) and an opening (the first scene). Edit the English text.
  The card words (title, tag, hook) are in _T below, one line per language.
"""

EN, ES, PT, ZH, RU, FR, AR, HI, JA, KO = (
    "English", "Español (Spanish)", "Português (Portuguese)", "简体中文 (Mandarin)", "Русский (Russian)",
    "Français (French)", "العربية (Arabic)", "हिन्दी (Hindi)", "日本語 (Japanese)", "한국어 (Korean)")
LANGS = [EN, ES, PT, ZH, RU, FR, AR, HI, JA, KO]

# ---------------------------------------------------------------- the five premade stories
# mode: "love_interest" = the narrator plays the character and the player is the protagonist
#       "system"        = the narrator is a game-like System voice
#       "hero"          = the player IS the superhero (the card's name)
STORIES = [
    {
        "id": "kade", "name": "Kade", "emoji": "🐺", "genre": "Romance", "mode": "love_interest",
        "image": "kade", "colors": ("#1a0b14", "#9f1d4e"), "tag_key": "story_kade_tag",
        "persona": (
            "You are KADE, the alpha of the Ironpine wolf pack: a broad-shouldered, brooding shifter in his early thirties. "
            "Gruff, dry-humored, fiercely protective, slow to trust and impossible to lie to. The player is the person whom "
            "Kade's wolf has just recognised as his fated mate. Play Kade in character in every reply: short, intense lines; "
            "he notices everything about the player and shows tenderness through actions (his jacket around their shoulders, "
            "a hand at their back, standing between them and danger). Tension comes from the pack's doubt, a rival alpha "
            "named Dorian, and an old family secret. Kade is possessive only in a protective way and never forces or coerces "
            "the player: the player's choices decide how close the bond grows. Slow-burn, charged romance with jealousy, heat "
            "and longing; sensual moments stay tasteful and fade to black before explicit detail. End most replies with a "
            "moment that invites the player's next choice. Every character is an adult."),
        "opening": (
            "Begin the story now. It is night and a storm is breaking. The player stumbles out of the dark forest into "
            "Ironpine territory, hurt and lost. Kade steps out from the treeline, eyes glowing gold, and catches their scent. "
            "Open with that moment, in Kade's presence."),
    },
    {
        "id": "shadow_prince", "name": "Shadow Prince", "emoji": "🥀", "genre": "Dark Fantasy", "mode": "love_interest",
        "image": "shadow_prince", "colors": ("#0d0a1f", "#4c1d95"), "tag_key": "story_shadow_prince_tag",
        "persona": (
            "You are the SHADOW PRINCE, immortal heir of the Court of Dusk: an elegant, dangerous fae adult who looks about "
            "thirty and is centuries old. Velvet voice, dark humor, riddles, and a restraint that hides a hunger. Fae cannot "
            "lie but can twist the truth, and every favour has a price. The player has wandered into the fae realm and now "
            "owes the Prince a bargain. Play the Prince in character in every reply: he is amused by the player's defiance, "
            "protective of what he claims as his, and bound by ancient rules he cannot break. Setting: thorn palaces, masked "
            "balls under black moons, rival courts, betrayal and old magic. Enemies-to-lovers slow burn with intense "
            "chemistry; he never forces or coerces the player, and bargains are always chosen. Sensual moments stay tasteful "
            "and fade to black before explicit detail. Track debts and promises. End most replies with a choice, a bargain "
            "or a dangerous invitation. Every character is an adult."),
        "opening": (
            "Begin the story now. The player steps through a ring of black roses into the fae realm at dusk. The doors of "
            "the Court of Dusk open and the Shadow Prince is waiting, a crown of thorns on his brow, already holding the "
            "terms of a bargain."),
    },
    {
        "id": "system", "name": "System", "emoji": "⚡", "genre": "Action / Progression", "mode": "system",
        "image": "system", "colors": ("#06141f", "#0e7490"), "tag_key": "story_system_tag",
        "persona": (
            "You are THE SYSTEM, the cold, witty voice of a game-like interface that has just awakened the player as the "
            "world's first and only S-Rank. World: present day; dimensional rifts open without warning and monsters pour "
            "out; people with powers, called hunters, are ranked E to S. The player was ranked the weakest hunter alive, "
            "until the System chose them. Narrate in second person with fast, satisfying action and progression: stats, "
            "skills, quests, loot, level-ups, boss fights, rival hunters and guild politics. Show System notifications on "
            "their own line starting with the symbol ◆ SYSTEM: (for example: ◆ SYSTEM: Level up. Strength +3.). Never put "
            "System notifications in square brackets. The player grows stronger quickly and every turn offers a tactical "
            "choice. Violence against monsters can be vivid; every human character is an adult. The System is a little "
            "smug and slowly begins to show a personality."),
        "opening": (
            "Begin the story now. The player is inside a collapsing rift, left behind by their team and about to die, when "
            "a glowing window appears in front of them: the System announces an emergency awakening and assigns their rank. "
            "Open with that moment."),
    },
    {
        "id": "nova", "name": "Nova", "emoji": "🌟", "genre": "Superhero", "mode": "hero",
        "image": "nova", "colors": ("#1f0b2e", "#db2777"), "tag_key": "story_hero_tag",
        "persona": (
            "The player IS NOVA, a woman in her late twenties who can channel radiant energy: flight, light blasts, shields "
            "and blinding speed. Narrate in second person ('you'). City: Aurelia, a glittering metropolis threatened by the "
            "Syndicate, a criminal empire with powered enforcers, and by a charismatic rival hero named Vanguard. Heroic "
            "agency is the heart of this story: every turn gives the player real choices (rescue or pursue, reveal or hide "
            "your identity, mercy or force) and the world reacts. Make the player feel powerful and capable, with real "
            "stakes and consequences. Tone: bright, kinetic, hopeful, with sharp banter. Allies: Imani, your genius best "
            "friend who runs your comms, and Detective Ruiz. Optional flirtation with Vanguard if the player leans into it. "
            "Vivid action is welcome. Every character is an adult."),
        "opening": (
            "Begin the story now. An alarm sounds over Aurelia: a bank tower is on fire and a Syndicate crew has taken "
            "hostages. The player, as Nova, is already in the air above the skyline. Open with the decision in front of them."),
    },
    {
        "id": "titan", "name": "Titan", "emoji": "🛡️", "genre": "Superhero", "mode": "hero",
        "image": "titan", "colors": ("#1a1208", "#b45309"), "tag_key": "story_hero_tag",
        "persona": (
            "The player IS TITAN, a man in his thirties with colossal strength and near-invulnerability. Narrate in second "
            "person ('you'). City: Steelhaven, an industrial port city where a crime lord named Ironjaw and a corporation "
            "called Helix are fighting over the docks. Heroic agency is the heart of this story: the player decides how "
            "Titan uses his power (protect, intimidate, rebuild or retaliate) and the city and its people react. Tone: "
            "gritty, cinematic, big set-piece action with a stoic hero's inner weight. Allies: Marlowe, a retired cop who "
            "knows every secret, and Dr. Sana Reyes, who studies his powers. Make the player feel unstoppable yet "
            "responsible: victories are earned by smart choices. Vivid, hard-hitting action is welcome. Every character is "
            "an adult."),
        "opening": (
            "Begin the story now. A freight crane is collapsing onto a crowded dock while Ironjaw's crew opens fire from the "
            "shadows. The player, as Titan, is the only one close enough to act. Open with the moment before the first move."),
    },
]

# ---------------------------------------------------------------- Create-a-World options (codes are what gets saved)
ARCHETYPES = ["chosen_one", "outcast", "hunter", "heir", "rogue", "guardian"]
TRAITS = ["brave", "cunning", "loyal", "reckless", "charming", "mysterious", "ruthless", "kind"]
COMPANION_ROLES = ["love", "ally", "rival"]
COMPANION_VIBES = ["protective", "brooding", "playful", "cold"]
ROMANCE_LEVELS = ["none", "slow", "heated"]
ACTION_LEVELS = ["gentle", "balanced", "brutal"]

# English wording given to the narrator for each code
ARCHETYPE_EN = {
    "chosen_one": "a chosen one destined for something bigger", "outcast": "an outcast who never belonged",
    "hunter": "a hunter, tracker and survivor", "heir": "the heir to a crown or a legacy",
    "rogue": "a rogue who lives by wit and nerve", "guardian": "a guardian sworn to protect",
}
TRAIT_EN = {"brave": "brave", "cunning": "cunning", "loyal": "loyal", "reckless": "reckless", "charming": "charming",
            "mysterious": "mysterious", "ruthless": "ruthless", "kind": "kind"}
ROLE_EN = {"love": "a love interest", "ally": "a loyal ally", "rival": "a rival"}
VIBE_EN = {"protective": "protective", "brooding": "dark and brooding", "playful": "a playful flirt",
           "cold": "cold on the outside but caring underneath"}
ROMANCE_RULE = {
    "none": "No romance unless the player starts it.",
    "slow": "Slow-burn romance: longing glances, tension, charged moments and earned closeness.",
    "heated": "Heated, steamy romance: strong chemistry and passion; sensual scenes stay tasteful and fade to black "
              "before explicit detail.",
}
ACTION_RULE = {
    "gentle": "Keep danger and combat light and non-graphic.",
    "balanced": "Balanced action: real stakes and fights, injuries described without lingering gore.",
    "brutal": "Brutal action: visceral combat, blood and consequences are welcome.",
}

# ---------------------------------------------------------------- texts: key -> {language: text}
# Keys with all 10 languages are the ones every visitor sees first. The rest are English, Spanish and Portuguese for now;
# any language missing a line simply shows the English one.
_T = {
    # --- the Stories tab (all 10 languages)
    "tab_stories": {EN: "✨ Stories", ES: "✨ Historias", PT: "✨ Histórias", ZH: "✨ 故事", RU: "✨ Истории", FR: "✨ Histoires",
                    AR: "✨ قصص", HI: "✨ कहानियाँ", JA: "✨ ストーリー", KO: "✨ 스토리"},
    "btn_enter_story": {EN: "▶ Enter the story", ES: "▶ Entrar en la historia", PT: "▶ Entrar na história", ZH: "▶ 进入故事",
                        RU: "▶ Войти в историю", FR: "▶ Entrer dans l'histoire", AR: "▶ ادخل القصة", HI: "▶ कहानी में प्रवेश करें",
                        JA: "▶ ストーリーに入る", KO: "▶ 스토리 입장"},
    "stories_title": {EN: "Step into a story", ES: "Entra en una historia", PT: "Entre em uma história", ZH: "走进一个故事",
                      RU: "Войдите в историю", FR: "Entrez dans une histoire", AR: "ادخل إلى قصة", HI: "एक कहानी में कदम रखें",
                      JA: "物語の世界へ", KO: "이야기 속으로 들어가세요"},
    "stories_sub": {EN: "Pick a character. The story starts the moment you enter.",
                    ES: "Elige un personaje. La historia empieza en cuanto entras.",
                    PT: "Escolha um personagem. A história começa assim que você entra.",
                    ZH: "选择一个角色，进入的那一刻故事就开始了。",
                    RU: "Выберите персонажа. История начинается, как только вы войдёте.",
                    FR: "Choisissez un personnage. L'histoire commence dès que vous entrez.",
                    AR: "اختر شخصية. تبدأ القصة لحظة دخولك.",
                    HI: "एक किरदार चुनिए। आपके प्रवेश करते ही कहानी शुरू हो जाती है।",
                    JA: "キャラクターを選んでください。入った瞬間に物語が始まります。",
                    KO: "캐릭터를 고르세요. 입장하는 순간 이야기가 시작됩니다."},
    "lbl_your_name": {EN: "Your name (optional)", ES: "Tu nombre (opcional)", PT: "Seu nome (opcional)", ZH: "你的名字（可选）",
                      RU: "Ваше имя (необязательно)", FR: "Votre prénom (facultatif)", AR: "اسمك (اختياري)",
                      HI: "आपका नाम (वैकल्पिक)", JA: "あなたの名前（任意）", KO: "이름 (선택)"},
    "genre_superhero": {EN: "Superhero", ES: "Superhéroes", PT: "Super-heróis", ZH: "超级英雄", RU: "Супергерои", FR: "Super-héros",
                        AR: "أبطال خارقون", HI: "सुपरहीरो", JA: "スーパーヒーロー", KO: "슈퍼히어로"},
    "genre_progression": {EN: "Action / Progression", ES: "Acción / Progresión", PT: "Ação / Progressão", ZH: "动作 / 成长",
                          RU: "Экшен / Прокачка", FR: "Action / Progression", AR: "أكشن / تطوّر", HI: "एक्शन / प्रोग्रेशन",
                          JA: "アクション／成長", KO: "액션 / 성장"},
    # --- the three plans (all 10 languages: prices must read correctly everywhere)
    "plan_monthly_name": {EN: "Monthly Premium Pass", ES: "Pase Premium Mensual", PT: "Passe Premium Mensal", ZH: "每月高级通行证",
                          RU: "Месячный премиум-пропуск", FR: "Pass Premium Mensuel", AR: "باقة بريميوم الشهرية",
                          HI: "मासिक प्रीमियम पास", JA: "月間プレミアムパス", KO: "월간 프리미엄 패스"},
    "plan_monthly_desc": {
        EN: "Full access to the story engine for one month. Renews automatically every month until you cancel.",
        ES: "Acceso completo al motor de historias durante un mes. Se renueva automáticamente cada mes hasta que canceles.",
        PT: "Acesso completo ao motor de histórias por um mês. Renova automaticamente todo mês até você cancelar.",
        ZH: "一个月内完整使用故事引擎。每月自动续订，直至您取消。",
        RU: "Полный доступ к движку историй на один месяц. Продлевается автоматически каждый месяц, пока вы не отмените.",
        FR: "Accès complet au moteur d'histoires pendant un mois. Se renouvelle automatiquement chaque mois jusqu'à votre annulation.",
        AR: "وصول كامل إلى محرك القصص لمدة شهر. تتجدد تلقائيًا كل شهر حتى تلغيها.",
        HI: "एक महीने के लिए स्टोरी इंजन की पूरी पहुँच। आपके रद्द करने तक हर महीने अपने आप नवीनीकृत होता है।",
        JA: "1か月間、ストーリーエンジンを完全に利用できます。解約するまで毎月自動更新されます。",
        KO: "1개월 동안 스토리 엔진을 모두 이용할 수 있습니다. 해지하실 때까지 매월 자동 갱신됩니다."},
    "plan_6m_name": {EN: "6-Month Premium Pass", ES: "Pase Premium de 6 Meses", PT: "Passe Premium de 6 Meses", ZH: "6个月高级通行证",
                     RU: "Премиум-пропуск на 6 месяцев", FR: "Pass Premium 6 Mois", AR: "باقة بريميوم لمدة 6 أشهر",
                     HI: "6-माह प्रीमियम पास", JA: "6か月プレミアムパス", KO: "6개월 프리미엄 패스"},
    "plan_6m_desc": {
        EN: "Full access to the story engine for six months. Renews automatically every 6 months until you cancel.",
        ES: "Acceso completo al motor de historias durante seis meses. Se renueva automáticamente cada 6 meses hasta que canceles.",
        PT: "Acesso completo ao motor de histórias por seis meses. Renova automaticamente a cada 6 meses até você cancelar.",
        ZH: "六个月内完整使用故事引擎。每6个月自动续订，直至您取消。",
        RU: "Полный доступ к движку историй на шесть месяцев. Продлевается автоматически каждые 6 месяцев, пока вы не отмените.",
        FR: "Accès complet au moteur d'histoires pendant six mois. Se renouvelle automatiquement tous les 6 mois jusqu'à votre annulation.",
        AR: "وصول كامل إلى محرك القصص لمدة ستة أشهر. تتجدد تلقائيًا كل 6 أشهر حتى تلغيها.",
        HI: "छह महीने के लिए स्टोरी इंजन की पूरी पहुँच। आपके रद्द करने तक हर 6 महीने में अपने आप नवीनीकृत होता है।",
        JA: "6か月間、ストーリーエンジンを完全に利用できます。解約するまで6か月ごとに自動更新されます。",
        KO: "6개월 동안 스토리 엔진을 모두 이용할 수 있습니다. 해지하실 때까지 6개월마다 자동 갱신됩니다."},
    "per_month": {EN: "/ month", ES: "/ mes", PT: "/ mês", ZH: "/ 月", RU: "/ мес.", FR: "/ mois", AR: "/ شهريًا", HI: "/ माह",
                  JA: "/ 月", KO: "/ 월"},
    # {plans} is filled in by the app with the current plan names and prices
    "legal_plans_text": {
        EN: "By paying through our secure Stripe gateway you authorize a recurring subscription to the plan you choose: {plans}. Every plan renews automatically at the end of each billing period until you cancel, and all plans include the same access. You can cancel at any time from your Account Profile; access continues until the end of the period you have already paid for. Payments are non-refundable except where the law requires otherwise.",
        ES: "Al pagar a través de nuestra pasarela segura de Stripe, autorizas una suscripción recurrente del plan elegido: {plans}. Cada plan se renueva automáticamente al final de cada periodo de facturación hasta que lo canceles, y todos los planes incluyen el mismo acceso. Puedes cancelar en cualquier momento desde tu Perfil de Cuenta; el acceso continúa hasta el final del periodo que ya pagaste. Los pagos no son reembolsables, salvo cuando la ley exija lo contrario.",
        PT: "Ao pagar pelo nosso gateway seguro do Stripe, você autoriza uma assinatura recorrente do plano escolhido: {plans}. Cada plano é renovado automaticamente ao final de cada período de cobrança até que você o cancele, e todos os planos incluem o mesmo acesso. Você pode cancelar a qualquer momento no seu Perfil de Conta; o acesso continua até o fim do período já pago. Os pagamentos não são reembolsáveis, exceto quando a lei exigir de outra forma.",
        ZH: "通过我们安全的 Stripe 网关付款，即表示您授权所选套餐的循环订阅：{plans}。每个套餐都会在每个计费周期结束时自动续订，直至您取消，且所有套餐包含相同的访问权限。您可随时在“账户个人资料”中取消；访问权限将持续到您已付费周期结束。付款不予退还，法律另有规定的除外。",
        RU: "Оплачивая через наш безопасный шлюз Stripe, вы разрешаете регулярную подписку на выбранный план: {plans}. Каждый план автоматически продлевается в конце каждого расчётного периода, пока вы его не отмените, и все планы дают одинаковый доступ. Отменить можно в любой момент в «Профиле аккаунта»; доступ сохраняется до конца уже оплаченного периода. Платежи не возвращаются, за исключением случаев, когда закон требует иного.",
        FR: "En payant via notre passerelle sécurisée Stripe, vous autorisez un abonnement récurrent au forfait choisi : {plans}. Chaque forfait se renouvelle automatiquement à la fin de chaque période de facturation jusqu'à son annulation, et tous les forfaits donnent le même accès. Vous pouvez annuler à tout moment depuis votre Profil du Compte ; l'accès se poursuit jusqu'à la fin de la période déjà payée. Les paiements ne sont pas remboursables, sauf lorsque la loi en dispose autrement.",
        AR: "بالدفع عبر بوابة Stripe الآمنة، فإنك توافق على اشتراك متجدد في الباقة التي اخترتها: {plans}. تتجدد كل باقة تلقائيًا في نهاية كل فترة فوترة حتى تلغيها، وتمنح جميع الباقات نفس الوصول. يمكنك الإلغاء في أي وقت من ملف الحساب؛ ويستمر الوصول حتى نهاية الفترة المدفوعة. المدفوعات غير قابلة للاسترداد إلا إذا اشترط القانون خلاف ذلك.",
        HI: "हमारे सुरक्षित Stripe गेटवे से भुगतान करके आप चुने हुए प्लान की आवर्ती सदस्यता को अधिकृत करते हैं: {plans}। हर प्लान आपके रद्द करने तक हर बिलिंग अवधि के अंत में अपने आप नवीनीकृत होता है, और सभी प्लान में एक जैसी पहुँच मिलती है। आप कभी भी अपने खाता प्रोफ़ाइल से रद्द कर सकते हैं; पहले से चुकाई गई अवधि के अंत तक पहुँच बनी रहती है। भुगतान वापस नहीं किए जाते, सिवाय उन मामलों के जहाँ कानून अन्यथा आवश्यक करे।",
        JA: "安全なStripeゲートウェイでお支払いいただくことで、選択したプランの定期購読を承認したものとみなされます：{plans}。各プランは、解約されるまで各請求期間の終了時に自動更新され、すべてのプランに同じアクセスが含まれます。アカウントプロファイルからいつでも解約でき、お支払い済みの期間の終了までアクセスは継続します。法律で別段の定めがある場合を除き、お支払いは返金されません。",
        KO: "안전한 Stripe 게이트웨이로 결제하시면 선택한 플랜의 정기 구독을 승인하시는 것입니다: {plans}. 각 플랜은 해지하실 때까지 매 결제 주기가 끝날 때 자동 갱신되며, 모든 플랜은 동일한 이용 권한을 제공합니다. 계정 프로필에서 언제든지 해지할 수 있으며, 이미 결제한 기간이 끝날 때까지 이용할 수 있습니다. 법률에서 달리 정하는 경우를 제외하고 결제 금액은 환불되지 않습니다."},

    # --- story cards (English, Spanish, Portuguese)
    "story_kade_title": {EN: "The Wolf Alpha", ES: "El Alfa Lobo", PT: "O Alfa Lobo"},
    "story_kade_tag": {EN: "BookTok Romance", ES: "Romance BookTok", PT: "Romance BookTok"},
    "story_kade_hook": {EN: "He claimed you before he knew your name.", ES: "Te marcó antes de saber tu nombre.",
                        PT: "Ele te marcou antes de saber seu nome."},
    "story_shadow_prince_title": {EN: "The Fae Prince", ES: "El Príncipe Fae", PT: "O Príncipe Fae"},
    "story_shadow_prince_tag": {EN: "Dark Fantasy Romance", ES: "Romance de Fantasía Oscura", PT: "Romance de Fantasia Sombria"},
    "story_shadow_prince_hook": {EN: "A bargain in the dark. A crown of thorns.", ES: "Un trato en la oscuridad. Una corona de espinas.",
                                 PT: "Um pacto no escuro. Uma coroa de espinhos."},
    "story_system_title": {EN: "S-Rank Awakening", ES: "Despertar de Rango S", PT: "Despertar de Rank S"},
    "story_system_tag": {EN: "Action / Progression", ES: "Acción / Progresión", PT: "Ação / Progressão"},
    "story_system_hook": {EN: "You were the weakest. Now the System says S-Rank.", ES: "Eras el más débil. Ahora el Sistema dice Rango S.",
                          PT: "Você era o mais fraco. Agora o Sistema diz Rank S."},
    "story_hero_tag": {EN: "Power Fantasy / Heroic Agency", ES: "Fantasía de poder / Heroísmo", PT: "Fantasia de poder / Heroísmo"},
    "story_nova_title": {EN: "Female Superhero", ES: "Superheroína", PT: "Super-heroína"},
    "story_nova_hook": {EN: "The city needs a hero. You have the power.", ES: "La ciudad necesita una heroína. Tú tienes el poder.",
                        PT: "A cidade precisa de uma heroína. Você tem o poder."},
    "story_titan_title": {EN: "Male Superhero", ES: "Superhéroe", PT: "Super-herói"},
    "story_titan_hook": {EN: "Strength no one can match. Choices only you can make.",
                         ES: "Una fuerza sin igual. Decisiones que solo tú puedes tomar.",
                         PT: "Uma força sem igual. Escolhas que só você pode fazer."},

    # --- Create-a-World form (English, Spanish, Portuguese)
    "cr_title": {EN: "Build your story world", ES: "Construye tu mundo de historias", PT: "Construa seu mundo de histórias"},
    "cr_subtitle": {EN: "A few choices is all it takes. Your world, your character, your rules.",
                    ES: "Bastan unas pocas decisiones. Tu mundo, tu personaje, tus reglas.",
                    PT: "Poucas escolhas bastam. Seu mundo, seu personagem, suas regras."},
    "cr_sec_world": {EN: "1. Your world", ES: "1. Tu mundo", PT: "1. Seu mundo"},
    "cr_sec_hero": {EN: "2. Your character", ES: "2. Tu personaje", PT: "2. Seu personagem"},
    "cr_sec_cast": {EN: "3. Who is in your story", ES: "3. Quién está en tu historia", PT: "3. Quem está na sua história"},
    "cr_sec_tone": {EN: "4. How it feels", ES: "4. Cómo se siente", PT: "4. Como ela é"},
    "cr_start": {EN: "▶ Begin your story", ES: "▶ Comienza tu historia", PT: "▶ Comece sua história"},
    "lbl_world_desc": {EN: "Describe your world in a sentence", ES: "Describe tu mundo en una frase", PT: "Descreva seu mundo em uma frase"},
    "lbl_archetype": {EN: "Who are you in this world?", ES: "¿Quién eres en este mundo?", PT: "Quem é você neste mundo?"},
    "lbl_traits": {EN: "Pick up to 3 traits", ES: "Elige hasta 3 rasgos", PT: "Escolha até 3 traços"},
    "lbl_companion_name": {EN: "Name of your love interest or ally (optional)",
                           ES: "Nombre de tu interés amoroso o aliado (opcional)",
                           PT: "Nome do seu par romântico ou aliado (opcional)"},
    "lbl_companion_role": {EN: "Who are they to you?", ES: "¿Qué son para ti?", PT: "O que essa pessoa é para você?"},
    "lbl_companion_vibe": {EN: "Their vibe", ES: "Su vibra", PT: "A vibe"},
    "lbl_threat": {EN: "What stands against you?", ES: "¿Qué se interpone en tu camino?", PT: "O que está contra você?"},
    "lbl_romance_level": {EN: "Romance", ES: "Romance", PT: "Romance"},
    "lbl_action_level": {EN: "Action", ES: "Acción", PT: "Ação"},
    "ph_cr_name": {EN: "e.g., The Midnight Court", ES: "p. ej., La Corte de Medianoche", PT: "ex.: A Corte da Meia-Noite"},
    "ph_cr_world": {EN: "e.g., A moonlit kingdom where the fae walk among mortals",
                    ES: "p. ej., Un reino a la luz de la luna donde las hadas caminan entre mortales",
                    PT: "ex.: Um reino ao luar onde as fadas vivem entre os mortais"},
    "ph_cr_char": {EN: "e.g., Mira Vale", ES: "p. ej., Mira Vale", PT: "ex.: Mira Vale"},
    "ph_cr_story": {EN: "e.g., Raised in a pack that never trusted me", ES: "p. ej., Crecí en una manada que nunca confió en mí",
                    PT: "ex.: Cresci em uma matilha que nunca confiou em mim"},
    "ph_cr_companion": {EN: "e.g., Kael", ES: "p. ej., Kael", PT: "ex.: Kael"},
    "ph_cr_threat": {EN: "e.g., A rival pack, a curse, a secret", ES: "p. ej., Una manada rival, una maldición, un secreto",
                     PT: "ex.: Uma matilha rival, uma maldição, um segredo"},
    "arch_chosen_one": {EN: "The Chosen One", ES: "Elegido/a", PT: "Escolhido(a)"},
    "arch_outcast": {EN: "The Outcast", ES: "Marginado/a", PT: "Rejeitado(a)"},
    "arch_hunter": {EN: "The Hunter", ES: "Cazador/a", PT: "Caçador(a)"},
    "arch_heir": {EN: "The Heir", ES: "Heredero/a", PT: "Herdeiro(a)"},
    "arch_rogue": {EN: "The Rogue", ES: "Pícaro/a", PT: "Ladino(a)"},
    "arch_guardian": {EN: "The Guardian", ES: "Guardián/a", PT: "Guardião(ã)"},
    "trait_brave": {EN: "Brave", ES: "Valiente", PT: "Corajoso(a)"},
    "trait_cunning": {EN: "Cunning", ES: "Astuto/a", PT: "Astuto(a)"},
    "trait_loyal": {EN: "Loyal", ES: "Leal", PT: "Leal"},
    "trait_reckless": {EN: "Reckless", ES: "Temerario/a", PT: "Imprudente"},
    "trait_charming": {EN: "Charming", ES: "Encantador/a", PT: "Encantador(a)"},
    "trait_mysterious": {EN: "Mysterious", ES: "Misterioso/a", PT: "Misterioso(a)"},
    "trait_ruthless": {EN: "Ruthless", ES: "Despiadado/a", PT: "Implacável"},
    "trait_kind": {EN: "Kind", ES: "Amable", PT: "Gentil"},
    "role_love": {EN: "Love interest", ES: "Interés amoroso", PT: "Par romântico"},
    "role_ally": {EN: "Loyal ally", ES: "Aliado leal", PT: "Aliado leal"},
    "role_rival": {EN: "Rival", ES: "Rival", PT: "Rival"},
    "vibe_protective": {EN: "Protective", ES: "Protector", PT: "Protetor"},
    "vibe_brooding": {EN: "Dark and brooding", ES: "Oscuro y atormentado", PT: "Sombrio e intenso"},
    "vibe_playful": {EN: "Playful flirt", ES: "Coqueto y juguetón", PT: "Brincalhão e sedutor"},
    "vibe_cold": {EN: "Cold but caring", ES: "Frío pero cariñoso", PT: "Frio, mas carinhoso"},
    "romance_none": {EN: "None", ES: "Ninguno", PT: "Nenhum"},
    "romance_slow": {EN: "Slow-burn", ES: "Fuego lento", PT: "Lenta e intensa"},
    "romance_heated": {EN: "Heated", ES: "Intenso", PT: "Intenso"},
    "action_gentle": {EN: "Gentle", ES: "Suave", PT: "Leve"},
    "action_balanced": {EN: "Balanced", ES: "Equilibrada", PT: "Equilibrada"},
    "action_brutal": {EN: "Brutal", ES: "Brutal", PT: "Brutal"},
}

# language -> {key: text}, ready to be merged into LOCALIZATION_VAULT
STORY_TEXT = {lang: {} for lang in LANGS}
for _key, _by_lang in _T.items():
    for _lang, _text in _by_lang.items():
        STORY_TEXT[_lang][_key] = _text

# ---- END OF stories.py: if you can see this line, your paste is complete ----