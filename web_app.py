import streamlit as st
import os
import re
import time
import stripe
import requests
import replicate  # 🚀 CHOSEN ENGINE: Loads the fast, indie-hacker approved image creation tool
from openai import OpenAI
from supabase import create_client, Client
from dotenv import load_dotenv

# 1. CORE ENGINE PAGE INITIALIZATION (MUST STAY AT THE TOP)
st.set_page_config(page_title="Haymaker Hub", page_icon="🪐", layout="wide")

# 🌐 LOCALIZATION VAULT - BLOCK 1: CORE CHANNELS (FULLY REMAPPED)
LOCALIZATION_VAULT = {
        "English": {
        "tab_explore": "🌐 Explore Universes", "tab_my_creations": "📂 My Creations", "tab_create": "🚀 Create a World", "tab_avatars": "🎭 Community Avatars", "tab_profile": "🔑 Account Profile", "status_control": "📡 STATUS CONTROL",
        "form_title": "### ⚔️ Universe Architect Form", "form_subtitle": "Tune the fundamental mechanics of your custom timeline before initializing the narrative seed.",
        "lbl_celestial": "##### 🪐 Celestial Physics", "lbl_name": "Universe Name:", "lbl_genre": "Select thematic genre:", "lbl_gravity": "🪐 Gravity Levels", "lbl_atmosphere": "💨 Atmospheric Density",
        "lbl_identity": "##### 🎭 Character Identity Settings", "lbl_char_name": "Your character's name:", "lbl_backstory": "Character profile/backstory:",
        "lbl_factions": "##### 🦅 Faction Architecture & Frictional Elements", "lbl_allies": "🦅 Dominant / Allied Faction Name", "lbl_enemies": "💀 Rogue / Opposing Faction Name", "lbl_directives": "✍️ Custom Environmental Directives / Constraints",
        "btn_deploy": "🚀 Deploy and Ignite Core Engine", "msg_success": "🎉 Custom universe timeline seed compiled successfully!",
        "genres": ["Sci-Fi", "Dark Fantasy", "Cyberpunk", "Horror", "Romance", "Other"],
        "atmosphere_options": ["Vacuum (Space)", "Thin / Toxic", "Breathable Baseline", "Hyper-Dense / Corrosive"],
        "trial_active": "⏳ TRIAL ACTIVE: {} Actions Left", "pool_depleted": "🔒 Action Pool Depleted!", "premium_pilot": "👑 PREMIUM PILOT AUTHENTICATED: {}",
        "active_records_title": "#### 👥 Active Community Records", "your_identity_title": "##### 👑 YOUR ACTIVE FORGED IDENTITY", "allied_dreamers_title": "##### 👥 ALLIED TIMELINE DREAMERS", "empty_ledger": "✨ The public ledger is currently empty. Be the first to forge a custom avatar identity asset above!", "signin_prompt": "🔑 Please sign in via the 'Account Profile' tab to view live character assets and authorize database ledger streams.",
        "dreamer_lbl": "Dreamer... {}", "music_prompt": "🎵 To listen to music, join or forge a world timeline", "unlimited_actions": "Want unlimited actions?", "btn_signin": "Sign In", "btn_signup": "Sign Up", "settings_control": "⚙️ Settings Control", "sub_genre_title": "🌌 Select Your Timeline Variant", "community_timeline_title": "📜 Public Community Timeline", "btn_join_world": "⚡ Enter This World Timeline",
        "auth_title": "### 🔑 Secure Identification Portal", "auth_subtitle": "Authorize your profile identity node to save custom timelines and clear limits.",
        "lbl_email": "Account Email Vector:", "lbl_pass": "Secure Password Signature:", "btn_login_submit": "🔐 Authorize Corridor Session", "btn_register_submit": "🚀 Forge New Profile Identity",
        "sub_genres_lbls": ["Sci-Fi", "Dark Fantasy", "Cyberpunk", "Horror", "Romance", "Other"],
        "btn_launch_scenario": "🎮 Launch Scenario",
        "settings_sub_status_title": "💳 Subscription Status",
        "settings_status_free": "⏳ STATUS: Free Trial Mode (12 Actions)",
        "settings_resync_title": "📡 Re-Sync Past Purchases",
        "settings_resync_desc": "Changed phones or reinstalled? Tap below to scan Stripe for your active billing cycle account profiles.",
        "settings_footer": "Haymaker Industry Security Architecture v1.02 • Privacy Framework Protected.",
        "hub_title": "🪐 Haymaker Industry Hub",
        "hub_subtitle": "Explore alternate realities or forge your own timeline",
        "profile_sync_lbl": "👑 Secure Profile Synchronized",
        "btn_logout_sidebar": "🚪 Log Out",
        "btn_logout_main": "🚪 Log Out of Platform Account"
    },
    "Español (Spanish)": {
        "tab_explore": "🌐 Explorar Universos", "tab_my_creations": "📂 Mis Creaciones", "tab_create": "🚀 Crear un Universo", "tab_avatars": "🎭 Avatares de la Comunidad", "tab_profile": "🔑 Perfil de Cuenta", "status_control": "📡 CONTROL DE ESTADO",
        "form_title": "### ⚔️ Formulario de Arquitecto del Universo", "form_subtitle": "Ajusta las mecánicas fundamentales de tu línea de tiempo antes de inicializar la semilla narrativa.",
        "lbl_celestial": "##### 🪐 Física Celestial", "lbl_name": "Nombre del Universo:", "lbl_genre": "Selecciona el género temático:", "lbl_gravity": "🪐 Niveles de Gravedad", "lbl_atmosphere": "💨 Densidad Atmosférica",
        "lbl_identity": "##### 🎭 Configuración de Identidad de Personaje", "lbl_char_name": "Nombre de tu personaje:", "lbl_backstory": "Perfil/Trasfondo del personaje:",
        "lbl_factions": "##### 🦅 Arquitetura de Facciones y Elementos de Fricción", "lbl_allies": "🦅 Nombre de la Facción Dominante / Aliada", "lbl_enemies": "💀 Nombre de la Facción Rebelde / Enemiga", "lbl_directives": "✍️ Directivas / Restricciones Ambientales Personalizadas",
        "btn_deploy": "🚀 Desplegar e Encender el Motor Central", "msg_success": "🎉 ¡Semilla de la línea de tiempo del universo compilada con éxito!",
        "genres": ["Ciencia Ficción", "Fantasía Oscura", "Cyberpunk", "Terror", "Romance", "Otro"],
        "atmosphere_options": ["Vacío (Espaço)", "Delgada / Tóxica", "Línea Base Respirable", "Hiperdensa / Corrosiva"],
        "trial_active": "⏳ PRUEBA ACTIVA: {} Acciones Restantes", "pool_depleted": "🔒 ¡Pool de Acciones Agotado!", "premium_pilot": "👑 PILOTO PREMIUM AUTENTICADO: {}",
        "active_records_title": "#### 👥 Registros Activos de la Comunidad", "your_identity_title": "##### 👑 TU IDENTIDAD ACTIVA FORJADA", "allied_dreamers_title": "##### 👥 SOÑADORES DE LÍNEAS DE TIEMPO ALIADAS", "empty_ledger": "✨ El registro público está actualmente vacío. ¡Sé el primero en forjar un avatar de identidad personalizado arriba!", "signin_prompt": "🔑 Inicie sesión a través de la pestaña 'Perfil de cuenta' para ver los activos de los personagens en vivo.",
        "dreamer_lbl": "Soñador... {}", "music_prompt": "🎵 Para escuchar música, únete o forja una línea de tiempo mundial", "unlimited_actions": "¿Quieres acciones ilimitadas?", "btn_signin": "Iniciar Sesión", "btn_signup": "Registrarse", "settings_control": "⚙️ Control de Configuración", "sub_genre_title": "🌌 Selecciona Tu Variante de Línea de Tiempo", "community_timeline_title": "📜 Línea de Tiempo Pública de la Comunidad", "btn_join_world": "⚡ Ingresar a Esta Línea de Tiempo",
        "auth_title": "### 🔑 Portal de Identificación Seguro", "auth_subtitle": "Autorice su nodo de identidad de perfil para guardar líneas de tiempo personalizadas.",
        "lbl_email": "Correo Electrónico de la Cuenta:", "lbl_pass": "Contraseña de Seguridad:", "btn_login_submit": "🔐 Autorizar Sesión del Corredor", "btn_register_submit": "🚀 Forjar Nueva Identidad de Perfil",
        "sub_genres_lbls": ["Ciencia Ficción", "Fantasía Oscura", "Cyberpunk", "Terror", "Romance", "Otro"],
        "btn_launch_scenario": "🎮 Iniciar Escenario",
        "settings_sub_status_title": "💳 Estado de la Suscripción",
        "settings_status_free": "⏳ ESTADO: Modo de Prueba Gratuita (12 Acciones)",
        "settings_resync_title": "📡 Sincronizar Compras Pasadas",
        "settings_resync_desc": "¿Cambió de teléfono o reinstaló? Toque a continuación para escanear Stripe en busca de sus perfiles de cuenta de ciclo de facturación activos.",
        "settings_footer": "Arquitectura de Seguridad de Haymaker Industry v1.02 • Marco de Privacidad Protegido.",
        "hub_title": "🪐 Eje Central de Haymaker Industry",
        "hub_subtitle": "Explora realidades alternativas o forja tu propia línea de tiempo",
        "profile_sync_lbl": "👑 Perfil Seguro Sincronizado",
        "btn_logout_sidebar": "🚪 Cerrar Sesión",
        "btn_logout_main": "🚪 Cerrar Sesión de la Cuenta de la Plataforma"
    },

            "简体中文 (Mandarin)": {
        "tab_explore": "🌐 探索宇宙", "tab_my_creations": "📂 我的创作", "tab_create": "🚀 创造世界", "tab_avatars": "🎭 社区化身", "tab_profile": "🔑 账户个人资料", "status_control": "📡 状态控制",
        "form_title": "### 宇宙架构师表单", "form_subtitle": "在初始化叙事种子之前，调整自定义时间线的基础机制。",
        "lbl_celestial": "##### 🪐 天体物理学", "lbl_name": "宇宙名称:", "lbl_genre": "选择主题类型:", "lbl_gravity": "🪐 引力水平", "lbl_atmosphere": "💨 大气密度",
        "lbl_identity": "##### 🎭 角色身份设置", "lbl_char_name": "你的角色名称:", "lbl_backstory": "角色档案/背景故事:",
        "lbl_factions": "##### 🦅 阵营架构与摩擦元素", "lbl_allies": "🦅 主导/盟友阵营名称", "lbl_enemies": "💀 叛军/敌对阵营名称", "lbl_directives": "✍️ 自定义环境指令/限制",
        "btn_deploy": "🚀 部署并启动核心引擎", "msg_success": "🎉 自定义宇宙时间线种子成功编译！",
        "genres": ["科幻", "黑暗奇幻", "赛博朋克", "恐怖", "浪漫", "其他"],
        "atmosphere_options": ["真空 (太空)", "稀薄 / 有毒", "可呼吸基准线", "高密度 / 腐蚀性"],
        "trial_active": "⏳ 试用激活：剩余 {} 次操作", "pool_depleted": "🔒 操作次数已耗尽！", "premium_pilot": "👑 已认证的高级试点员：{}",
        "active_records_title": "#### 👥 活跃社区记录", "your_identity_title": "##### 👑 您当前处于激活状态的化身", "allied_dreamers_title": "##### 👥 盟友时间线追梦人", "empty_ledger": "✨ 公共账本目前为空。成为第一个在上方锻造自定义头像身份资产的人！", "signin_prompt": "🔑 请通过“账户个人资料”标签登录以查看实时角色资产并授权数据库账本流。",
        "dreamer_lbl": "追梦人... {}", "music_prompt": "🎵 要听音乐，请加入或打造 world 时间线", "unlimited_actions": "想要无限操作次数吗？", "btn_signin": "登录", "btn_signup": "注册", "settings_control": "⚙️ 设置控制", "sub_genre_title": "🌌 选择您的时间线变体", "community_timeline_title": "📜 公共社区时间线", "btn_join_world": "⚡ 进入此世界时间线",
        "auth_title": "### 🔑 安全身份验证门户", "auth_subtitle": "授权您的个人资料身份节点以保存自定义时间线并清除限制。",
        "lbl_email": "账户电子邮件:", "lbl_pass": "安全密码签名:", "btn_login_submit": "🔐 授权通道会话", "btn_register_submit": "🚀 锻造新个人身份",
        "sub_genres_lbls": ["科幻小说", "黑暗幻想", "赛博朋克", "恐怖", "浪漫", "其他"],
        "btn_launch_scenario": "🎮 启动场景",
        "settings_sub_status_title": "💳 订阅状态",
        "settings_status_free": "⏳ 状态：免费 trial 模式 (12 次操作)",
        "settings_resync_title": "📡 重新同步历史购买",
        "settings_resync_desc": "更换了手机或重新安装？点击下方扫描 Stripe 以获取您处于活跃计费周期的账户档案。",
        "settings_footer": "Haymaker Industry 安全架构 v1.02 • 隐私框架保护。",
        "hub_title": "🪐 Haymaker Industry 中心枢纽",
        "hub_subtitle": "探索交错现实或锻造属于您自己的时间线",
        "profile_sync_lbl": "👑 安全 profile 已同步",
        "btn_logout_sidebar": "🚪 退出登录",
        "btn_logout_main": "🚪 退出平台账户"
    }
}
# 🌐 LOCALIZATION VAULT - BLOCK 2: RUSSIAN, FRENCH, ARABIC EXPANSIONS
LOCALIZATION_VAULT.update({
    "Русский (Russian)": {
        "tab_explore": "🌐 Обзор Вселенных", "tab_my_creations": "📂 Мои Творения", "tab_create": "🚀 Создать Мир", "tab_avatars": "🎭 Аватары Сообщества", "tab_profile": "🔑 Профиль Аккаунта", "status_control": "📡 МОНИТОР СТАТУСА",
        "form_title": "### ⚔️ Форма Архитектора Вселенной", "form_subtitle": "Настройте фундаментальную механику вашей временной шкалы перед запуском повествовательного семени.",
        "lbl_celestial": "##### 🪐 Небесная Физика", "lbl_name": "Название Вселенной:", "lbl_genre": "Выберите жанр:", "lbl_gravity": "🪐 Уровни Гравитации", "lbl_atmosphere": "💨 Плотность Атмосферы",
        "lbl_identity": "##### 🎭 Настройки Личности Персонажа", "lbl_char_name": "Имя вашего персонажа:", "lbl_backstory": "Профиль/Биография персонажа:",
        "lbl_factions": "##### 🦅 Архитектура Фракций и Элементы Трения", "lbl_allies": "🦅 Имя Доминирующей Фракции", "lbl_enemies": "💀 Имя Враждебной Фракции", "lbl_directives": "✍️ Особые Директивы и Ограничения Мира",
        "btn_deploy": "🚀 Развернуть и Запустить Ядро", "msg_success": "🎉 Семя вселенной успешно скомпилировано!",
        "genres": ["Фантастика", "Темное Фэнтези", "Киберпанк", "Хоррор", "Романтика", "Другое"],
        "atmosphere_options": ["Вакуум (Космос)", "Тонкая / Токсичная", "Дыхательный Базис", "Плотная / Коррозийная"],
        "trial_active": "⏳ ПРОБНЫЙ ПЕРИОД: Осталось {} действий", "pool_depleted": "🔒 Пул действий исчерпан!", "premium_pilot": "👑 ПРЕМИУМ-ПИЛОТ АВТОРИЗОВАН: {}",
        "active_records_title": "#### 👥 Активные Записи Сообщества", "your_identity_title": "##### 👑 ВАШ АКТИВНЫЙ АВАТАР", "allied_dreamers_title": "##### 👥 СОЮЗНЫЕ СТРАННИКИ ВРЕМЕНИ", "empty_ledger": "✨ Публичный реестр пуст.", "signin_prompt": "🔑 Пожалуйста, войдите в аккаунт.",
        "dreamer_lbl": "Мечтатель... {}", "music_prompt": "🎵 Чтобы слушать музыку, войдите в мир", "unlimited_actions": "Хотите безлимит?", "btn_signin": "Войти", "btn_signup": "Регистрация", "settings_control": "⚙️ Настройки", "sub_genre_title": "🌌 Выберите вариант временной шкалы", "community_timeline_title": "📜 Публичная хроника сообщества", "btn_join_world": "⚡ Войти в этот мир",
        "auth_title": "### 🔑 Безопасный портал идентификации", "auth_subtitle": "Авторизуйте свой идентификационный узел.",
        "lbl_email": "Электронная почта:", "lbl_pass": "Пароль:", "btn_login_submit": "🔐 Авторизовать сессию коридора", "btn_register_submit": "🚀 Создать новый профиль",
        "sub_genres_lbls": ["Научная фантастика", "Темное фэнтези", "Киберпанк", "Ужасы", "Романтика", "Другое"],
        "btn_launch_scenario": "🎮 Запустить сценарий",
        "settings_sub_status_title": "💳 Статус подписки",
        "settings_status_free": "⏳ СТАТУС: Режим бесплатной версии (12 действий)",
        "settings_resync_title": "📡 Синхронизация прошлых покупок",
        "settings_resync_desc": "Поменяли телефон или переустановили? Нажмите ниже, чтобы отсканировать Stripe на наличие активных профилей биллинга.",
        "settings_footer": "Архитектура безопасности Haymaker Industry v1.02 • Защищено структурой конфиденциальности.",
        "hub_title": "🪐 Главный хаб Haymaker Industry",
        "hub_subtitle": "Исследуйте альтернативные реальности или создайте свою временную шкалу",
        "profile_sync_lbl": "👑 Безопасный профиль синхронизирован",
        "btn_logout_sidebar": "🚪 Выйти",
        "btn_logout_main": "🚪 Выйти из аккаунта платформы"
    },

        "Français (French)": {
        "tab_explore": "🌐 Explorer les Univers", "tab_my_creations": "📂 Mes Créations", "tab_create": "🚀 Créer un Monde", "tab_avatars": "🎭 Avatars de la Communauté", "tab_profile": "🔑 Profil du Compte", "status_control": "📡 CONTRÔLE DE STATUT",
        "form_title": "### ⚔️ Formulaire d'Architecte d'Univers", "form_subtitle": "Ajustez les mécaniques fondamentales de votre chronologie avant d'initialiser le code narratif.",
        "lbl_celestial": "##### 🪐 Physique Céleste", "lbl_name": "Nom de l'Univers:", "lbl_genre": "Sélectionnez le genre:", "lbl_gravity": "🪐 Niveaux de Gravité", "lbl_atmosphere": "💨 Densité Atmosphérique",
        "lbl_identity": "##### 🎭 Paramètres d'Identité du Personnage", "lbl_char_name": "Nom de votre personnage:", "lbl_backstory": "Profil/Histoire du personnage:",
        "lbl_factions": "##### 🦅 Architecture des Factions & Éléments de Friction", "lbl_allies": "🦅 Nom de la Faction Dominante / Alliée", "lbl_enemies": "💀 Nom de la Faction Ennemie", "lbl_directives": "✍️ Directives / Contraintes Environnementales Spécifiques",
        "btn_deploy": "🚀 Déployer et Activer le Moteur Central", "msg_success": "🎉 Le code de l'univers a été compilé avec succès !",
        "genres": ["Sci-Fi", "Dark Fantasy", "Cyberpunk", "Horreur", "Romance", "Autre"],
        "atmosphere_options": ["Vide (Espace)", "Mince / Toxique", "Atmosphère Respirable", "Hyper-Dense / Corrosive"],
        "trial_active": "⏳ ESSAI ACTIF: {} Actions Restantes", "pool_depleted": "🔒 Pool d'Actions Épuisé !", "premium_pilot": "👑 PILOTE PREMIUM AUTHENTIFIÉ: {}",
        "active_records_title": "#### 👥 Registres Actifs de la Communauté", "your_identity_title": "##### 👑 VOTRE IDENTITÉ ACTIVE", "allied_dreamers_title": "##### 👥 REVEURS CHRONOLOGIQUES ALLIÉS", "empty_ledger": "✨ Le registre public est vide.", "signin_prompt": "🔑 Veuillez vous connecter pour voir les enregistrements.",
        "dreamer_lbl": "Rêveur... {}", "music_prompt": "🎵 Pour écouter de la musique, rejoignez un monde", "unlimited_actions": "Actions illimitées ?", "btn_signin": "Connexion", "btn_signup": "S'inscrire", "settings_control": "⚙️ Réglages", "sub_genre_title": "🌌 Sélectionnez votre variante", "community_timeline_title": "📜 Chronologie publique", "btn_join_world": "⚡ Rejoindre ce monde",
        "auth_title": "### 🔑 Portail d'Identification Séquentiel Sécurisé", "auth_subtitle": "Autorisez votre nœud d'identité pour sauvegarder vos univers.",
        "lbl_email": "Email du Compte:", "lbl_pass": "Mot de Passe Sécurisé:", "btn_login_submit": "🔐 Autoriser la Session", "btn_register_submit": "🚀 Forger une Nouvelle Identité",
        "sub_genres_lbls": ["Sci-Fi", "Dark Fantasy", "Cyberpunk", "Horreur", "Romance", "Autre"],
        "btn_launch_scenario": "🎮 Lancer le Scénario",
        "settings_sub_status_title": "💳 Statut de l'Abonnement",
        "settings_status_free": "⏳ STATUT : Mode d'Essai Gratuit (12 Actions)",
        "settings_resync_title": "📡 Re-synchroniser les Achats Passés",
        "settings_resync_desc": "Changement de téléphone ou réinstallation ? Appuyez ci-dessous pour scanner Stripe pour vos profils de compte de cycle de facturation actifs.",
        "settings_footer": "Architecture de Securité de Haymaker Industry v1.02 • Cadre de Confidentialité Protégé.",
        "hub_title": "🪐 Hub Central de Haymaker Industry",
        "hub_subtitle": "Explorez des réalités alternatives ou forgez votre propre chronologie",
        "profile_sync_lbl": "👑 Profil Sécurisé Synchronisé",
        "btn_logout_sidebar": "🚪 Se Déconnecter",
        "btn_logout_main": "🚪 Se Déconnecter du Compte de la Plateforme"
    },

    "العربية (Arabic)": {
        "tab_explore": "🌐 استكشاف العوالم", "tab_my_creations": "📂 إبداعاتي", "tab_create": "🚀 صنع عالمًا", "tab_avatars": "🎭 شخصيات المجتمع", "tab_profile": "🔑 ملف الحساب", "status_control": "📡 مراقبة الحالة",
        "form_title": "### ⚔️ نموذج مهندس الكون", "form_subtitle": "قم بضبط الآليات الأساسية لخطك الزمني قبل تهيئة النواة السردية.",
        "lbl_celestial": "##### 🪐 الفيزياء الفلكية", "lbl_name": "اسم الكون:", "lbl_genre": "اختر نوع القصة:", "lbl_gravity": "🪐 مستويات الجاذبية", "lbl_atmosphere": "💨 كثافة الغلاف الجوي",
        "lbl_identity": "##### 🎭 إعدادات هوية الشخصية", "lbl_char_name": "اسم شخصيتك:", "lbl_backstory": "ملف الشخصية / الخلفية الدرامية:",
        "lbl_factions": "##### 🦅 بنية الفصائل وعناصر الاحتكاك", "lbl_allies": "🦅 اسم الفصيل الحليف / المسيطر", "lbl_enemies": "💀 اسم الفصيل المعادي", "lbl_directives": "✍️ توجيهات وقيود بيئية مخصصة",
        "btn_deploy": "🚀 نشر وتفعيل المحرك الرئيسي", "msg_success": "🎉 تم تجميع نواة الكون المخصص بنجاح!",
        "genres": ["خيال علمي", "فانتازيا مظلمة", "سايبربانك", "رعب", "رومانسي", "آخر"],
        "atmosphere_options": ["فراغ (الفضاء)", "رقيق / سام", "قابل للتنفس", "كثيف جدًا / أكّال"],
        "trial_active": "⏳ الفترة التجريبية: متبقي {} إجراءات", "pool_depleted": "🔒 تم استنفاد رصيد الإجراءات!", "premium_pilot": "👑 تم التحقق من الطيار المتميز: {}",
        "active_records_title": "#### 👥 سجلات المجتمع推力", "your_identity_title": "##### 👑 هويتك النشطة الحالية", "allied_dreamers_title": "##### 👥 الحالمون في الخطوط الزمنية الحليفة", "empty_ledger": "✨ السجل العام فارغ حاليًا.", "signin_prompt": "🔑 يرجى تسجيل الدخول لعرض السجلات.",
        "dreamer_lbl": "الحالم... {}", "music_prompt": "🎵 للاستماع للموسيقى，انضم لعالم", "unlimited_actions": "تريد إجراءات غير محدودة؟", "btn_signin": "تسجيل الدخول", "btn_signup": "إنشاء حساب", "settings_control": "⚙️ التحكم بالإعدادات", "sub_genre_title": "🌌 اختر بديل الخط الزمني", "community_timeline_title": "📜 الخط الزمني العام للمجتمع", "btn_join_world": "⚡ دخول هذا الخط الزمني",
        "auth_title": "### 🔑 بوابة التحقق الآمنة", "auth_subtitle": "قم بترخيص معرفك الشخصي لحفظ الخطوط الزمنية وتخطي القيود.",
        "lbl_email": "البريد الإلكتروني:", "lbl_pass": "كلمة المرور الآمنة:", "btn_login_submit": "🔐 ترخيص جلسة الممر", "btn_register_submit": "🚀 إنشاء هوية جديدة",
        "sub_genres_lbls": ["خيال علمي", "فانتازيا مظلمة", "سايبربانك", "رعب", "رومانسي", "آخر"],
        "btn_launch_scenario": "🎮 بدء السيناريو",
        "settings_sub_status_title": "💳 حالة الاشتراك",
        "settings_status_free": "⏳ الحالة: وضع الفترة التجريبية المجانية (12 إجراء)",
        "settings_resync_title": "📡 إعادة مزامنة المشتريات السابقة",
        "settings_resync_desc": "هل قمت بتغيير هاتفك أو إعادة التثبيت؟ اضغط أدناه لمسح Stripe بحثًا عن ملفات تعريف حساب دورة الفوترة النشطة.",
        "settings_footer": "بنية Haymaker Industry الأمنية إصدار v1.02 • إطار الخصوصية المحمي.",
        "hub_title": "🪐 مركز Haymaker Industry الرئيسي",
        "hub_subtitle": "استكشف العوالم البديلة أو اصنع خطك الزمني الخاص",
        "profile_sync_lbl": "👑 تم مزامنة الملف الشخصي الآمن",
        "btn_logout_sidebar": "🚪 تسجيل الخروج",
        "btn_logout_main": "🚪 تسجيل الخروج من حساب المنصة"
    }
})

## 🌐 LOCALIZATION VAULT - BLOCK 3: HINDI, JAPANESE, KOREAN ASIA POWERHOUSES
LOCALIZATION_VAULT.update({
    "हिन्दी (Hindi)": {
        "tab_explore": "🌐 ब्रह्मांड खोजें", "tab_my_creations": "📂 मेरी रचनाएँ", "tab_create": "🚀 ब्रह्मांड बनाएं", "tab_avatars": "🎭 समुदाय अवतार", "tab_profile": "🔑 खाता प्रोफ़ाइल", "status_control": "📡 स्थिति नियंत्रण",
        "form_title": "### ⚔️ ब्रह्मांड आर्किटेक्ट फॉर्म", "form_subtitle": "कथा बीज शुरू करने से पहले अपनी समयरेखा के बुनियादी तंत्र को ट्यून करें.",
        "lbl_celestial": "##### 🪐 खगोलीय भौतिकी", "lbl_name": "ब्रह्मांड का नाम:", "lbl_genre": "शैली चुनें:", "lbl_gravity": "🪐 गुरुत्वाकर्षण स्तर", "lbl_atmosphere": "💨 वायुमंडलीय घनत्व",
        "lbl_identity": "##### 🎭 चरित्र पहचान सेटिंग्स", "lbl_char_name": "आपके चरित्र का नाम:", "lbl_backstory": "चरित्र प्रोफ़ाइल:",
        "lbl_factions": "##### 🦅 गुट वास्तुकला", "lbl_allies": "🦅 प्रमुख गुट का नाम", "lbl_enemies": "💀 विरोधी गुट का नाम", "lbl_directives": "✍️ कस्टम निर्देश",
        "btn_deploy": "🚀 कोर इंजन तैनात करें", "msg_success": "🎉 ब्रह्मांड समयरेखा सफलतापूर्वक संकलित की गई!",
        "genres": ["साइंस-फिक्शन", "डार्क फंतासी", "साइबरपंक", "हॉरर", "रोमांस", "अन्य"],
        "atmosphere_options": ["वैक्यूम (अंतरिक्ष)", "पतली / जहरीली", "सांस लेने योग्य", "अत्यधिक घनी"],
        "trial_active": "⏳ परीक्षण सक्रिय: {} क्रियाएं शेष", "pool_depleted": "🔒 क्रिया पूल समाप्त!", "premium_pilot": "👑 प्रीमियम पायलट प्रमाणित: {}",
        "active_records_title": "#### 👥 सक्रिय समुदाय रिकॉर्ड", "your_identity_title": "##### 👑 आपकी सक्रिय पहचान", "allied_dreamers_title": "##### 👥 संबद्ध सपने देखने वाले", "empty_ledger": "✨ सार्वजनिक खाता खाली है.", "signin_prompt": "🔑 कृपया रिकॉर्ड देखने के लिए लॉग इन करें.",
        "dreamer_lbl": "सपने देखने वाला... {}", "music_prompt": "🎵 संगीत सुनने के लिए, ब्रह्मांड से जुड़ें", "unlimited_actions": "असीमित क्रियाएं चाहिए?", "btn_signin": "लॉग इन करें", "btn_signup": "साइन अप करें", "settings_control": "⚙️ सेटिंग्स नियंत्रण", "sub_genre_title": "🌌 अपना समयरेखा संस्करण चुनें", "community_timeline_title": "📜 सार्वजनिक समुदाय समयरेखा", "btn_join_world": "⚡ इस ब्रह्मांड में प्रवेश करें",
        "auth_title": "### 🔑 सुरक्षित पहचान पोर्टल", "auth_subtitle": "अपनी प्रोफ़ाइल पहचान को अधिकृत करें.",
        "lbl_email": "खाता ईमेल:", "lbl_pass": "सुरक्षित पासवर्ड:", "btn_login_submit": "🔐 कॉरिडोर सत्र अधिकृत करें", "btn_register_submit": "🚀 नई पहचान का निर्माण करें",
        "sub_genres_lbls": ["साइंस-फिक्शन", "डार्क फंतासी", "साइबरपंक", "हॉरर", "रोमांस", "अन्य"],
        "btn_launch_scenario": "🎮 परिदृश्य लॉन्च करें",
        "settings_sub_status_title": "💳 सदस्यता की स्थिति",
        "settings_status_free": "⏳ स्थिति: मुफ़्त परीक्षण मोड (12 क्रियाएं)",
        "settings_resync_title": "📡 पिछली खरीदारी को पुन: सिंक करें",
        "settings_resync_desc": "फोन बदल दिया या फिर से इंस्टॉल किया? अपने सक्रिय बिलिंग चक्र खाता प्रोफाइल के लिए स्ट्राइप को स्कैन करने के लिए नीचे टैप करें।",
        "settings_footer": "Haymaker Industry सुरक्षा आर्किटेक्चर v1.02 • गोपनीयता ढांचा सुरक्षित।",
        "hub_title": "🪐 Haymaker Industry मुख्य हब",
        "hub_subtitle": "वैकल्पिक वास्तविकताओं का पता लगाएं या अपनी खुद की समयरेखा बनाएं",
        "profile_sync_lbl": "👑 सुरक्षित प्रोफ़ाइल सिंक्रनाइज़",
        "btn_logout_sidebar": "🚪 लॉग आउट",
        "btn_logout_main": "🚪 प्लेटफ़ॉर्म खाते से लॉग आउट करें"
    },
    "日本語 (Japanese)": {
        "tab_explore": "🌐 タイムライン探索", "tab_my_creations": "📂 マイユニバース", "tab_create": "🚀 世界の創造", "tab_avatars": "🎭 コミュニティ共同体", "tab_profile": "🔑 アカウントプロファイル", "status_control": "📡 ステータス管理",
        "form_title": "### ⚔️ 世界設計アーキテクトフォーム", "form_subtitle": "物語 of シードを初期化する前に、カスタムタイムラインの根本的なメカニズムを調整します。",
        "lbl_celestial": "##### 🪐 天体物理学パラメーター", "lbl_name": "世界・固有名称:", "lbl_genre": "テーマジャンル選択:", "lbl_gravity": "🪐 重力係数", "lbl_atmosphere": "💨 大気濃度レイヤー",
        "lbl_identity": "##### 🎭 キャラクター固有アイデンティティ", "lbl_char_name": "プレイヤーキャラクター名:", "lbl_backstory": "キャラクタープロファイル/背景設定:",
        "lbl_factions": "##### 🦅 勢力アーキテクチャ & 摩擦対立エレメント", "lbl_allies": "🦅 支配勢力 / 同盟クラン名称", "lbl_enemies": "💀 反乱勢力 / 敵対組織名称", "lbl_directives": "✍️ 固有環境指令 / 世界の制約・ルール",
        "btn_deploy": "🚀 世界線構築エンジン点火", "msg_success": "🎉 カスタムタイムラインの構築に成功しました！",
        "genres": ["SF", "ダークファンタジー", "サイバーパンク", "ホラー", "ロマンス", "その他"],
        "atmosphere_options": ["真空 (宇宙)", "希薄 / 有毒", "標準呼吸可能環境", "超高密度 / 腐食性"],
        "trial_active": "⏳ トライアル有効: 残り {} アクション", "pool_depleted": "🔒 アクションプールが枯渇しました！", "premium_pilot": "👑 認定プレミアムパイロット: {}",
        "active_records_title": "#### 👥 アクティブなタイムライン記録", "your_identity_title": "##### 👑 あなたの現在のアバター", "allied_dreamers_title": "##### 👥 同盟関係の時空観測者", "empty_ledger": "✨ パブリックレジャーは現在空です。", "signin_prompt": "🔑 アカウントプロファイルからログインしてください。",
        "dreamer_lbl": "観測者... {}", "music_prompt": "🎵 音楽を聴くには世界線に参加してください", "unlimited_actions": "無制限のアクセスを解放しますか？", "btn_signin": "ログイン", "btn_signup": "新規登録", "settings_control": "⚙️ 制御システム", "sub_genre_title": "🌌 タイムラインのバリアントを選択", "community_timeline_title": "📜 パブリックコミュニティタイムライン", "btn_join_world": "⚡ この世界線にダイブする",
        "auth_title": "### 🔑 セキュア身元認証ポータル", "auth_subtitle": "プロファイルを認証します。",
        "lbl_email": "メールアドレス:", "lbl_pass": "安全なパスワード:", "btn_login_submit": "🔐 セッション接続を承認", "btn_register_submit": "🚀 新規観測者アイデンティティを鍛造",
        "sub_genres_lbls": ["SF", "ダークファンタジー", "サイバーパンク", "ホラー", "ロマンス", "その他"],
        "btn_launch_scenario": "🎮 シナリオを起動",
        "settings_sub_status_title": "💳 サブスクリプションステータス",
        "settings_status_free": "⏳ ステータス: 無料トライアルモード (残り12アクション)",
        "settings_resync_title": "📡 過去の購入を再同期",
        "settings_resync_desc": "機種変更または再インストールしましたか？以下をタップしてStripeをスキャンし、アクティブな課金サイクルアカウントを確認します。",
        "settings_footer": "Haymaker Industry セキュリティアーキテクチャ v1.02 • プライバシーフレームワーク保護",
        "hub_title": "🪐 Haymaker Industry 総合ハブ",
        "hub_subtitle": "仮想現実を探索、またはあなた自身のタイムラインを構築",
        "profile_sync_lbl": "👑 セキュアなプロファイルが同期されました",
        "btn_logout_sidebar": "🚪 ログアウト",
        "btn_logout_main": "🚪 プラットフォームアカウントからログアウト"
    },


       "한국어 (Korean)": {
        "tab_explore": "🌐 세계선 탐색", "tab_my_creations": "📂 나의 창작물", "tab_create": "🚀 세계 창조", "tab_avatars": "🎭 커뮤니티 아바타", "tab_profile": "🔑 계정 프로필", "status_control": "📡 상태 제어 센터",
        "form_title": "### ⚔️ 세계 설계 아키텍트 폼", "form_subtitle": "서사 시드를 초기화하기 전에 커스텀 시간선의 기본 메커니즘을 조정하십시오.",
        "lbl_celestial": "##### 🪐 우주 물리학 매개변수", "lbl_name": "세계선 이름:", "lbl_genre": "테마 장르 선택:", "lbl_gravity": "🪐 중력 수치", "lbl_atmosphere": "💨 대기 밀도",
        "lbl_identity": "##### 🎭 캐릭터 신원 설정", "lbl_char_name": "캐릭터 이름:", "lbl_backstory": "캐릭터 프로필:",
        "lbl_factions": "##### 🦅 세력 아키텍처 & 마찰 대립 요소", "lbl_allies": "🦅 지배 세력 진영 이름", "lbl_enemies": "💀 반란 진영 이름", "lbl_directives": "✍️ 커스텀 환경 지침",
        "btn_deploy": "🚀 코어 엔진 배포 및 점화", "msg_success": "🎉 우주 시간선 시드가 성공적으로 컴파일되었습니다!",
        "genres": ["SF", "다크 판타지", "사이버펑크", "공포", "로맨스", "기타"],
        "atmosphere_options": ["진공 (우주)", "희박 / 유독", "호흡 가능 기준선", "초고밀도 / 부식성"],
        "trial_active": "⏳ 체험판 활성화: {}회 작업 남음", "pool_depleted": "🔒 작업 풀이 모두 소진되었습니다!", "premium_pilot": "👑 인증된 프리미엄 파일럿: {}",
        "active_records_title": "#### 👥 활성화된 커뮤니티 기록", "your_identity_title": "##### 👑 현재 활성화된 아바타", "allied_dreamers_title": "##### 👥 동맹 시간선의 관측자들", "empty_ledger": "✨ 공개 장부가 비어 있습니다.", "signin_prompt": "🔑 로그인 후 실시간 캐릭터 자산을 확인하세요.",
        "dreamer_lbl": "관측자... {}", "music_prompt": "🎵 음악을 들으려면 세계선에 참여하세요", "unlimited_actions": "무제한 작업을 원하십니까?", "btn_signin": "로그인", "btn_signup": "회원가입", "settings_control": "⚙️ 설정 제어", "sub_genre_title": "🌌 시간선 변체 선택", "community_timeline_title": "📜 공개 타임라인", "btn_join_world": "⚡ 이 세계선으로 진입",
        "auth_title": "### 🔑 보안 신원 인증 포털", "auth_subtitle": "프로필을 인증하십시오.",
        "lbl_email": "계정 이메일:", "lbl_pass": "보안 비밀번호:", "btn_login_submit": "🔐 통로 세션 승인", "btn_register_submit": "🚀 새로운 신원 생성",
        "sub_genres_lbls": ["SF", "다크 판타지", "사이버펑크", "공포", "로맨스", "기타"],
        "btn_launch_scenario": "🎮 시나리오 시작",
        "settings_sub_status_title": "💳 구독 상태",
        "settings_status_free": "⏳ 상태: 무료 체험 모드 (12회 남음)",
        "settings_resync_title": "📡 과거 구매 내역 재동기화",
        "settings_resync_desc": "휴대폰을 변경했거나 재설치하셨나요? 아래를 탭하여 Stripe에서 활성 결제 주기 계정 프로필을 스캔하세요.",
        "settings_footer": "Haymaker Industry 보안 아키텍처 v1.02 • 개인정보 보호 프레임워크 적용",
        "hub_title": "🪐 Haymaker Industry 중앙 허브",
        "hub_subtitle": "가상 현실을 탐색하거나 자신만의 시간선을 구축하십시오",
        "profile_sync_lbl": "👑 보안 프로필이 동기화되었습니다",
        "btn_logout_sidebar": "🚪 로그아웃",
        "btn_logout_main": "🚪 플랫폼 계정에서 로그아웃"
    },
    "Português (Portuguese)": {
        "tab_explore": "🌐 Explorar Universos", "tab_my_creations": "📂 Minhas Criações", "tab_create": "🚀 Criar um Mundo", "tab_avatars": "🎭 Avatares da Comunidade", "tab_profile": "🔑 Perfil de Conta", "status_control": "📡 CONTROLE DE STATUS",
        "form_title": "### ⚔️ Formulário do Arquiteto do Universo", "form_subtitle": "Ajuste a mecânica fundamental da sua linha do tempo antes de inicializar a semente narrativa.",
        "lbl_celestial": "##### 🪐 Física Celestial", "lbl_name": "Nome do Universo:", "lbl_genre": "Selecione o gênero temático:", "lbl_gravity": "🪐 Níveis de Gravidade", "lbl_atmosphere": "💨 Densidade Atmosférica",
        "lbl_identity": "##### 🎭 Configuração de Identidade do Personagem", "lbl_char_name": "Nome do seu personagem:", "lbl_backstory": "Perfil/Histórico do personagem:",
        "lbl_factions": "##### 🦅 Arquitetura de Facções e Elementos de Fricção", "lbl_allies": "🦅 Nome da Facção Dominante / Aliada", "lbl_enemies": "💀 Nome da Facção Rebelde / Inimiga", "lbl_directives": "✍️ Diretrizes / Restrições Ambientais Personalizadas",
        "btn_deploy": "🚀 Implantar e Acender o Motor Central", "msg_success": "🎉 Semente da linha do tempo do universo compilada com sucesso!",
        "genres": ["Ficção Científica", "Fantasia Sombria", "Cyberpunk", "Terror", "Romance", "Outro"],
        "atmosphere_options": ["Vácuo (Espaço)", "Rara / Tóxica", "Linha de Base Respirável", "Hipertensa / Corrosiva"],
        "trial_active": "⏳ TESTE ATIVO: {} Ações Restantes", "pool_depleted": "🔒 Pool de Ações Esgotado!", "premium_pilot": "👑 PILOTO PREMIUM AUTENTICADO: {}",
        "active_records_title": "#### 👥 Registros Ativos da Comunidade", "your_identity_title": "##### 👑 SUA IDENTIDADE ATIVA FORJADA", "allied_dreamers_title": "##### 👥 SONHADORES DE LINHAS DO TEMPO ALIADAS", "empty_ledger": "✨ O registro público está atualmente vazio. Seja o primeiro a forjar uma identidade acima!", "signin_prompt": "🔑 Por favor, faça login na aba 'Perfil de Conta' para ver os registros dos personagens ao vivo.",
        "dreamer_lbl": "Sonhador... {}", "music_prompt": "🎵 Para ouvir música, junte-se ou forje uma linha do tempo mundial", "unlimited_actions": "Quer ações ilimitadas?", "btn_signin": "Entrar", "btn_signup": "Cadastrar-se", "settings_control": "⚙️ Controle de Configurações", "sub_genre_title": "🌌 Selecione Sua Variante de Linha do Tempo", "community_timeline_title": "📜 Linha do Tempo Pública da Comunidade", "btn_join_world": "⚡ Entrar Neste Universo da Comunidade",
        "auth_title": "### 🔑 Portal de Identificação Secure", "auth_subtitle": "Autorize seu nó de identidade de perfil para salvar linhas do tempo personalizadas.",
        "lbl_email": "E-mail da Conta:", "lbl_pass": "Senha de Segurança:", "btn_login_submit": "🔐 Autorizar Sessão", "btn_register_submit": "🚀 Forjar Nova Identidade de Perfil",
        "sub_genres_lbls": ["Ficção Científica", "Fantasia Sombria", "Cyberpunk", "Terror", "Romance", "Outro"],
        "btn_launch_scenario": "🎮 Iniciar Cenário",
        "settings_sub_status_title": "💳 Status da Assinatura",
        "settings_status_free": "⏳ STATUS: Modo de Teste Gratuito (12 Ações)",
        "settings_resync_title": "📡 Re-sincronizar Compras Passadas",
        "settings_resync_desc": "Mudou de telefone ou reinstalou? Toque abaixo para escanear o Stripe em busca de perfis de conta com ciclo de faturamento ativo.",
        "settings_footer": "Arquitetura de Segurança da Haymaker Industry v1.02 • Estrutura de Privacidade Protegida.",
        "hub_title": "🪐 Hub Central da Haymaker Industry",
        "hub_subtitle": "Explore realidades alternativas ou forje a sua própria linha do tempo",
        "profile_sync_lbl": "👑 Perfil Seguro Sincronizado",
        "btn_logout_sidebar": "🚪 Sair",
        "btn_logout_main": "🚪 Sair da Conta da Plataforma"
    }
}) # 🚨 MASTER DICTIONARY VAULT UPDATE SECURELY CLOSED AND PINNED


    




# 🌐 GLOBAL LOCALIZATION STATE RUNWAY INITIALIZATION
if "app_language" not in st.session_state:
    st.session_state["app_language"] = None

# 📡 SYSTEM CORES INITIALIZATION: Anchor default states before any layout elements render
if "world_cover_url" not in st.session_state:
    st.session_state["world_cover_url"] = "https://picsum.photos"

if "guest_tokens" not in st.session_state:
    st.session_state["guest_tokens"] = 12  # Standard trial buffer fallback safety state

# 🎵 LOCAL CUSTOM AUDIOSCAPE STORAGE INITIALIZATION
if "audio_state" not in st.session_state:
    st.session_state.audio_state = {
        "playing": True, 
        "track_url": "assets/menu_theme.mp3"  # Points to your fresh custom campaign file!
    }
# 🚨 LAYOUT RE-ALIGNMENT FLUSH MATRICES
if "render_alignment_fixed" not in st.session_state:
    st.session_state.render_alignment_fixed = True
    st.cache_data.clear()  # Hard clears modern Streamlit internal data buffers



# ---------------------------------------------------------
# 🌐 THE ENTERPRISE LOCALIZATION CHECKPOINT GATEWAY (FRONT GATE)
# ---------------------------------------------------------
if st.session_state.get("app_language") is None:
    st.markdown("# ⚔️ HAYMAKER INDUSTRY")
    st.markdown("""
    <div style="background: rgba(16, 12, 31, 0.6); padding: 24px; border-radius: 16px; border: 1px solid #3b2c63; margin-bottom: 25px;">
        <h3 style="color: #ffffff; margin: 0 0 10px 0; font-family: monospace; letter-spacing: 1px; font-size: 18px;">🪐 SELECT YOUR STRUCTURAL LANGUAGE MATRIX</h3>
        <p style="color: #94a3b8; font-size: 13px; margin: 0 0 20px 0; line-height: 1.6;">
            Establish your dynamic profile localization interface parameters before entering the sandbox workspace.
        </p>
        <hr style="border-color: #2e234e; margin-bottom: 20px;">
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px; font-family: monospace; font-size: 12px; color: #a78bfa;">
            <div>• English (US / Global)</div>
            <div>• Español (Seleccione Su Idioma)</div>
            <div>• 简体中文 (请选择您的语言)</div>
            <div>• Русский (Выберите ваш язык)</div>
            <div>• Français (Choisissez votre langue)</div>
            <div>• العربية (اختر لغة الواجهة)</div>
            <div>• हिन्दी (अपनी भाषा चुनें)</div>
            <div>• 日本語 (インターフェース言語の選択)</div>
            <div>• 한국어 (인터페이스 언어 선택)</div>
            <div>• Português (Selecione o seu idioma)</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    
    # 🪐 STEP 1 UPGRADE: Expanded list layout to capture all 9 major global traffic streams
    selected_matrix_lang = st.selectbox(
        "🌐 Choose Interface Language Node / Seleccione Su Idioma / 请选择您的语言:",
        [
           "English", "Español (Spanish)", "简体中文 (Mandarin)", "Русский (Russian)", "Français (French)", "العربية (Arabic)", "हिन्दी (Hindi)", "日本語 (Japanese)", "한국어 (Korean)", "Português (Portuguese)"

        ],
        key="sb_global_onboarding_language_picker"
    )

    
    if st.button("🚀 IGNITE APPLICATION INTERFACE", use_container_width=True):
        st.session_state.app_language = selected_matrix_lang
        
        # 👑 SECURE PROFILE SYNC: Save choice if authenticated
        if "user" in st.session_state:
            try:
                if "access_token" in st.session_state:
                    supabase_client.postgrest.auth(st.session_state["access_token"])
                supabase_client.table("profiles").upsert({
                    "id": st.session_state.user.id,
                    "interface_language": str(selected_matrix_lang)
                }).execute()
            except Exception:
                pass
                
        st.success(f"⚡ Interface matrix locked to {selected_matrix_lang}! Syncing layout scales...")
        time.sleep(1.0)
        st.rerun()
        
    st.stop() # 🛑 ABSOLUTE EMERGENCY BREAK: Freezes the layout completely right here so sidebars/tabs stay hidden!


# GLOBAL THEME DESIGN: High-Contrast Modern Tech Dynamic UI Skin
st.markdown("""
<style>
    .stApp {
        background-color: #05030a !important;
        background-image: none !important;
        color: #f8fafc !important;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    }
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #cbd5e1 0%, #a2adb9 50%, #788596 100%) !important;
        border-right: 2px solid #2e1566 !important;
        box-shadow: inset -4px 0px 12px rgba(0,0,0,0.25), 4px 0px 20px rgba(0,0,0,0.4) !important;
    }
    [data-testid="stSidebar"] p, [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h3, [data-testid="stSidebar"] label {
        color: #0f172a !important; font-weight: 700 !important;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 14px; background-color: #020005 !important; padding: 10px;
        border-radius: 24px; border: 1px solid #1e1538; box-shadow: inset 0 4px 12px rgba(0,0,0,0.6);
    }
    .stTabs [data-baseweb="tab"] {
        background: linear-gradient(180deg, #cbd5e1 0%, #cbd5e1 100%) !important;
        color: #0f172a !important; font-weight: 700 !important; text-transform: uppercase;
        letter-spacing: 0.8px; font-size: 13px !important; padding: 10px 24px !important;
        border-radius: 20px !important; border-top: 1px solid #ffffff !important;
        border-left: 1px solid #ffffff !important; border-right: 2px solid #64748b !important;
        border-bottom: 3px solid #475569 !important; box-shadow: 0 4px 8px rgba(0,0,0,0.3) !important;
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important; margin-bottom: 2px !important;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #4c1d95 0%, #1e1b4b 100%) !important;
        color: #ffffff !important; padding: 14px 28px !important; 
        border-top: 1px solid #7c5dfa !important; border-left: 1px solid #7c5dfa !important;
        border-right: 1px solid #0f172a !important; border-bottom: 1px solid #0f172a !important;
        box-shadow: inset 0px 4px 10px rgba(0,0,0,0.8), 0 0 20px rgba(124, 93, 250, 0.3) !important;
        transform: translateY(2px) !important;
    }
    .premium-discovery-card {
        background: #110c1f !important; border-radius: 20px !important;
        border-top: 1px solid #3b2c63 !important; border-left: 1px solid #3b2c63 !important;
        border-right: 2px solid #05020a !important; border-bottom: 4px solid #05020a !important;
        box-shadow: 0 10px 20px rgba(0,0,0,0.5) !important; margin-bottom: 24px !important;
        overflow: hidden !important; display: flex !important; flex-direction: column;
    }
    .sidebar-avatar-frame {
        width: 130px; height: 130px; background-color: #161026; border-radius: 40px !important;
        border-top: 2px solid #ffffff; border-left: 2px solid #ffffff;
        border-right: 2px solid #475569; border-bottom: 4px solid #1e293b;
        box-shadow: 0 6px 12px rgba(0,0,0,0.3); margin: 16px auto;
        display: flex; align-items: center; justify-content: center; font-size: 50px;
    }
    .stButton > button {
        background: linear-gradient(180deg, #cbd5e1 0%, #94a3b8 100%) !important;
        color: #0f172a !important; font-weight: 700 !important; text-transform: uppercase;
        letter-spacing: 0.5px; border-radius: 18px !important; border-top: 1px solid #ffffff !important;
        border-left: 1px solid #ffffff !important; border-right: 2px solid #475569 !important;
        border-bottom: 4px solid #334155 !important; box-shadow: 0 4px 6px rgba(0,0,0,0.2) !important;
    }
    .stButton > button:hover {
        color: #ffffff !important; background: linear-gradient(180deg, #7c5dfa 0%, #5b21b6 100%) !important;
    }
    /* 🌌 IMMERSIVE LIVE CANVAS BACKGROUND OVERLAY MATRIX */
    .immersive-chat-viewport {
        background-position: center !important;
        background-size: cover !important;
        background-repeat: no-repeat !important;
        border-radius: 24px !important;
        padding: 24px !important;
        border: 1px solid rgba(124, 93, 250, 0.15) !important;
        box-shadow: inset 0 0 100px rgba(0,0,0,0.85), 0 20px 40px rgba(0,0,0,0.6) !important;
        margin-top: 16px !important;
    }
    /* Translucent frosted glass effect to keep reading text crisp and legible over any artwork */
    .glass-frosted-scroller {
        background-color: rgba(5, 3, 10, 0.75) !important;
        backdrop-filter: blur(12px) saturate(160%);
        -webkit-backdrop-filter: blur(12px) saturate(160%);
        border-radius: 20px !important;
        padding: 20px !important;
        border: 1px solid rgba(255, 255, 255, 0.05) !important;
    }
</style>
""", unsafe_allow_html=True)

load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")
STRIPE_SECRET = os.getenv("STRIPE_SECRET_KEY")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL")  # 🔒 Loaded safely into server memory


if not API_KEY or not SUPABASE_URL or not SUPABASE_KEY:
    st.error("🔒 Missing crucial core environment variables inside your hidden .env file!")
    st.stop()

openai_client = OpenAI(api_key=API_KEY)
supabase_client: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

if STRIPE_SECRET:
    stripe.api_key = STRIPE_SECRET

# POP-UP MODAL WINDOW GATEWAY
if "active_modal" in st.session_state and st.session_state.active_modal:
    modal = st.session_state.active_modal
    @st.dialog(modal["title"])
    def render_modal_window():
        st.image(modal["img"], use_container_width=True)
        st.markdown(f"**🎨 Creator ID Token:** `{modal['creator']}`")
        st.markdown(f"**🎭 Character Dossier Summary:** {modal['bio']}")
        if st.button("🚪 Close Dossier File", use_container_width=True):
            st.session_state.active_modal = None
            st.rerun()
    render_modal_window()

# STRIPE SUITE CHECKS
if "success" in st.query_params and st.query_params["success"] == "true":
    st.session_state.is_premium = True
    st.toast("👑 Premium Unlimited Pass Activated Successfully!")

# TRIAL VARIABLES STORAGE INITIALIZATION
if "user" not in st.session_state:
    if "guest_tokens" not in st.session_state:
        st.session_state.guest_tokens = 12  
    if "world_engine" not in st.session_state:
        st.session_state.world_engine = {
            "world_id": None, "world_name": "", "world_genre": "",
            "player_character": {"name": "", "backstory": "", "health": 100, "inventory": ["survival gear"]},
            "story_log": []
        }
else:
    st.session_state.guest_tokens = 999999  

engine = st.session_state.world_engine
char = engine["player_character"]
# ---------------------------------------------------------
# # 5. DYNAMIC SIDEBAR OVERWATCH PANEL
# ---------------------------------------------------------
with st.sidebar:
    # 🗺️ READ ACTIVE LOCALIZATION MATRIX STATES
    active_lang = st.session_state.get("app_language", "English")
    text_vault = LOCALIZATION_VAULT[active_lang]

    # 🪐 DYNAMIC LOCALIZED SIDEBAR BANNER
    st.title(text_vault["status_control"])
    st.divider()
    
    # 🚪 HOME TERMINAL ESCAPE GATEWAY (Fully Localized Routing Mapping Node)
    if engine["world_name"]:
        # Dynamic translate mappings for the abandon navigation button
        abandon_label = "🚪 ABANDON TIMELINE" if active_lang == "English" else ("🚪 ABANDONAR LÍNEA DE TIEMPO" if active_lang == "Español (Spanish)" else "🚪 放弃时间线")
        if st.button(abandon_label, type="secondary", key="sidebar_exit_timeline_gate", use_container_width=True):
            st.session_state.world_engine = {
                "world_id": None, "world_name": "", "world_genre": "",
                "player_character": {"name": "", "backstory": "", "health": 100, "inventory": ["survival gear"]},
                "story_log": []
            }
            if "world_cover_url" in st.session_state:
                st.session_state.world_cover_url = "https://picsum.photos"
            st.rerun()
        st.divider()

    # 🔐 PHASE 1 PROTOCOL: The Ironclad Paywall Vault Execution Checks
    if "user" in st.session_state:
        user_id = st.session_state.user.id
        
        # 📡 LIVE VAULT INVENTORY: Verify subscription metadata & language records directly from your database
        try:
            profile_query = supabase_client.table("profiles").select("is_premium, interface_language").eq("id", user_id).single().execute()
            
            if profile_query.data:
                is_premium = profile_query.data.get("is_premium", False)
                saved_lang = profile_query.data.get("interface_language")
                
                # 🪐 AUTOMATED PROFILE LOADING: Instantly lock in their saved language choice if it exists
                if saved_lang:
                    st.session_state.app_language = saved_lang
                    # Synchronize the lookup matrix mapping states right away
                    text_vault = LOCALIZATION_VAULT[saved_lang]
            else:
                is_premium = False
        except Exception:
            is_premium = False  # Strict default safety gate fallback position

               # 👑 THE PAYWALL GATEWAY: Halt non-paying accounts instantly, but bypass entirely for the Premium Pilot
        is_admin_override = False
        ADMIN_EMAIL = os.getenv("ADMIN_EMAIL")
        
        if "user" in st.session_state and ADMIN_EMAIL:
            if str(st.session_state.user.email).strip().lower() == str(ADMIN_EMAIL).strip().lower():
                is_admin_override = True

        # ⏳ TRIAL PROTOCOL ENFORCEMENT: Normal users only hit the wall once BOTH their premium pass and trial tokens are gone
        has_trial_tokens = st.session_state.get("guest_tokens", 0) > 0

        if not is_premium and not is_admin_override and not has_trial_tokens:
            # 🟢 BASIC USER RESTRICTION GATEWAY (Fires ONLY when trial tokens hit 0)
            if active_lang == "Español (Spanish)":
                st.markdown("### ⚔️ DESATA TU UNIVERSO")
                st.write("Para los que trabajan duro, los soñadores y los creadores: Trabajas duro. Ahora es el momento de jugar duro. Las aplicaciones corporativas censuran tu imaginación; este es tu santuario independiente y sin filtros. Desbloquea mundos infinitos, historias personalizadas y bandas sonoras atmosféricas al instante.")
                st.info("💡 Consejo profesional: Completa primero el marco de personalización del personaje y del mundo en la pestaña de opciones antes de activar el acceso.")
                btn_premium_text = "🚀 ACTIVAR PASE PREMIUM — $10 / SEMANA"
                warning_msg = "⚠️ Acceso pendiente: Una vez que su pago se procese correctamente, haga clic en el botón de abajo para verificar el estado de su token."
                btn_verify_text = "🔄 Verificar Estado del Token de Pago"
            elif active_lang == "简体中文 (Mandarin)":
                st.markdown("### ⚔️ 解放你的宇宙")
                st.write("献给苦干者、白日梦想家和创作者：你工作努力。现在是尽情玩耍的时候了。企业级应用会审查你的想象力——这是你未经过滤的独立避难所。立即解锁无限的文字冒险世界、自定义故事情节和环境原声带。")
                st.info("💡 专业提示：在激活访问权限之前，请先在选项标签中完成您的角色 and 世界架构自定义框架。")
                btn_premium_text = "🚀 激活尊享通行证 — $10 / 周"
                warning_msg = "⚠️ 访问挂起：您的 Stripe 交易处理完成后，请点击下方刷新按钮验证代币状态以解锁工作区。"
                btn_verify_text = "🔄 验证支付代币状态"
            else:
                st.markdown("### ⚔️ UNLEASH YOUR UNIVERSE")
                st.write("To grinders, daydreamers, and creators: You work hard. Now it's time to play hard. Corporate apps censor your imagination—this is your unfiltered independent sanctuary. Unlock infinite text-adventure worlds, custom storylines, and atmospheric soundtracks instantly.")
                st.info("💡 Pro Tip: Complete your character and world architecture customization framework in the options tab first to lock in your timeline blueprint before activating access.")
                btn_premium_text = "🚀 ACTIVATE PREMIUM PASS — $10 / WEEK"
                warning_msg = "⚠️ Access Pending: Once your Stripe transaction processes cleanly, click the refresh button below to verify your token state and unlock your sandbox canvas panel."
                btn_verify_text = "🔄 Verify Payment Token Status"
            
            stripe_checkout_url = "https://stripe.com"
            
            st.markdown(
                f'<a href="{stripe_checkout_url}" target="_blank" style="text-decoration: none;">'
                f'<div style="background-color: #00FF66; color: black; text-align: center; padding: 14px; '
                f'font-weight: bold; border-radius: 6px; font-size: 18px; margin-top: 15px; margin-bottom: 25px;">'
                f'{btn_premium_text}</div></a>',
                unsafe_allow_html=True
            )
            
            st.warning(warning_msg)
            if st.button(btn_verify_text, key="sidebar_payment_manual_verify_btn"):
                st.rerun()
                
            st.stop() # Stops execution ONLY for basic trial users who haven't paid and have 0 tokens


            
            st.warning(warning_msg)
            if st.button(btn_verify_text, key="sidebar_payment_manual_verify_btn"):
                st.rerun()
                
            st.stop() # ABSOLUTE EMERGENCY BREAK: Freezes execution instantly

        # 🟢 ACCESS GRANTED: Paid subscribers pass cleanly past the gate
        st.success(text_vault["premium_pilot"].format(st.session_state.user.email))
        
    else:
        if st.session_state.guest_tokens > 0:
            st.warning(text_vault["trial_active"].format(st.session_state.guest_tokens))
        else:
            st.error(text_vault["pool_depleted"])
            
    st.divider()

    
        # 🖼️ HOUSING FRAME FOR PLAYER PROFILE IMAGE
    avatar_display = "👤" if not engine["world_name"] else "🎭"
    st.markdown(f'<div class="sidebar-avatar-frame">{avatar_display}</div>', unsafe_allow_html=True)
    
    # 🪐 DYNAMIC LOCALIZED USERNAME DISPLAY TRACKER
    display_username = char["name"] if char["name"] else "Wanderer"
    
    # Extract the dynamic "Dreamer... {username}" text structure natively
    localized_dreamer_text = text_vault['dreamer_lbl'].format(display_username)
    
    st.markdown(
        f"<p style='text-align: center; font-size: 16px; margin: 0; color: white;'>"
        f"<span style='font-weight: 800; color: #a78bfa;'>{localized_dreamer_text}</span></p>", 
        unsafe_allow_html=True
    )
    
    st.divider()


    
        # 🎵 DYNAMIC SYSTEM AUDIO MATRICES DECK (Fully Localized Integration Matrix)
    # Determine the localized text for the mute and play action nodes
    btn_mute_lbl = "🔇 Mute Audio" if active_lang == "English" else ("🔇 Silenciar Audio" if active_lang == "Español (Spanish)" else "🔇 静音音频")
    btn_play_lbl = "🔊 Play Audio" if active_lang == "English" else ("🔊 Reproducir Audio" if active_lang == "Español (Spanish)" else "🔊 播放音频")

    with st.expander("🎵 AMBIENT AUDIOSCAPE", expanded=True):
        if not engine["world_name"]:
            # 🪐 DYNAMIC LOCALIZED MUSIC PROMPT: Automatically adapts to Spanish or Mandarin natively
            st.markdown(
                f"<p style='text-align: center; font-size: 13px; color: #a78bfa; font-weight: bold; margin: 5px 0;'>"
                f"{text_vault['music_prompt']}</p>", 
                unsafe_allow_html=True
            )
        else:
            col_m1, col_m2 = st.columns(2)
            with col_m1:
                if st.session_state.audio_state["playing"]:
                    if st.button(btn_mute_lbl, use_container_width=True, key="btn_mute_audio_chan"):
                        st.session_state.audio_state["playing"] = False
                        st.rerun()
                else:
                    if st.button(btn_play_lbl, use_container_width=True, key="btn_play_audio_chan"):
                        st.session_state.audio_state["playing"] = True
                        st.rerun()

                        
            with col_m2:
                # 🌎 DYNAMIC LOCALIZED NEXT TRACK LABELS
                if active_lang == "Español (Spanish)":
                    btn_next_lbl = "🔀 Siguiente Pista"
                elif active_lang == "简体中文 (Mandarin)":
                    btn_next_lbl = "🔀 下一首曲目"
                elif active_lang == "Русский (Russian)":
                    btn_next_lbl = "🔀 Следующий трек"
                elif active_lang == "Français (French)":
                    btn_next_lbl = "🔀 Piste Suivante"
                elif active_lang == "العربية (Arabic)":
                    btn_next_lbl = "🔀 المسار التالي"
                elif active_lang == "हिन्दी (Hindi)":
                    btn_next_lbl = "🔀 अगला ट्रैक"
                elif active_lang == "日本語 (Japanese)":
                    btn_next_lbl = "🔀 次のトラック"
                elif active_lang == "한국어 (Korean)":
                    btn_next_lbl = "🔀 다음 트랙"
                elif active_lang == "Português (Portuguese)":
                    btn_next_lbl = "🔀 Próxima Faixa"
                else:
                    btn_next_lbl = "🔀 Next Track"


                if st.button(btn_next_lbl, use_container_width=True, key="btn_next_audio_track"):
                    playlist_deck = [
                        "assets/menu_theme.mp3",
                        "assets/adventure_loop.mp3",
                        "assets/track_1.mp3", "assets/track_2.mp3", 
                        "assets/track_3.mp3", "assets/track_4.mp3",
                        "assets/track_5.mp3", "assets/track_6.mp3",
                        "assets/track_7.mp3", "assets/track_8.mp3"
                    ]
                    
                    current_track = st.session_state.audio_state["track_url"]
                    try:
                        current_index = playlist_deck.index(current_track)
                        next_index = (current_index + 1) % len(playlist_deck)
                    except ValueError:
                        next_index = 0
                    
                    chosen_track = playlist_deck[next_index]
                    if os.path.exists(chosen_track):
                        st.session_state.audio_state["track_url"] = chosen_track
                    else:
                        st.session_state.audio_state["track_url"] = "assets/menu_theme.mp3"
                        
                    st.session_state.audio_state["playing"] = True
                    st.rerun()
                    
            if st.session_state.audio_state["playing"]:
                st.audio(st.session_state.audio_state['track_url'], format="audio/mp3", loop=True)
                
                               # 🌎 DYNAMIC LOCALIZED STREAM AUTHORIZATION CAPTIONS
                if active_lang == "Español (Spanish)":
                    caption_lbl = "🔊 Haga clic en reproducir en el reproductor oficial para autorizar la transmisión"
                elif active_lang == "简体中文 (Mandarin)":
                    caption_lbl = "🔊 点击官方播放面板上的播放键以授权音频流"
                elif active_lang == "Русский (Russian)":
                    caption_lbl = "🔊 Нажмите кнопку воспроизведения на официальной панели для авторизации потока"
                elif active_lang == "Français (French)":
                    caption_lbl = "🔊 Cliquez sur lecture sur le lecteur officiel pour autoriser le flux"
                elif active_lang == "العربية (Arabic)":
                    caption_lbl = "🔊 انقر فوق تشغيل في اللوحة الرسمية للمصادقة على البث"
                elif active_lang == "हिन्दी (Hindi)":
                    caption_lbl = "🔊 स्ट्रीम को अधिकृत करने के लिए आधिकारिक डेक पर प्ले पर क्लिक करें"
                elif active_lang == "日本語 (Japanese)":
                    caption_lbl = "🔊 ストリーム配信を承認するには公式プレイヤーの再生ボタンを押してください"
                elif active_lang == "한국어 (Korean)":
                    caption_lbl = "🔊 스트림 스트리밍을 승인하려면 공식 데크에서 재생을 클릭하십시오"
                elif active_lang == "Português (Portuguese)":
                    caption_lbl = "🔊 Clique em reproduzir no player oficial para autorizar a transmissão"
                else:
                    caption_lbl = "🔊 Click play on the official deck to authorize stream"

                    
                st.caption(caption_lbl)
            else:
                st.markdown("<p style='font-size: 11px; text-align: center; color: #7f1d1d; margin: 10px 0 0 0; font-weight: bold;'>⚠️ System Audio Channel Disabled 🔴</p>", unsafe_allow_html=True)

    # SIDEBAR LOGIN & LOGOUT TOGGLE CONTROLS
    if "user" in st.session_state:
        if st.button("🚪 LOG OUT ACCOUNT", type="primary", key="sidebar_logout_gate", use_container_width=True):
            supabase_client.auth.sign_out()
            st.session_state.clear()
            st.rerun()
    else:
        st.info(text_vault.get("unlimited_actions", "💡 Want unlimited actions?"))

    # 🌎 DYNAMIC LOCALIZED COMBINED LABEL MATRIX
    signin_lbl = text_vault.get("btn_signin", "Sign In")
    signup_lbl = text_vault.get("btn_signup", "Sign Up")
    combined_auth_lbl = f"🔑 {signin_lbl.upper()} / {signup_lbl.upper()}"

    if st.button(combined_auth_lbl, key="sidebar_auth_gateway_redirect", use_container_width=True):
        # Dynamic multi-lingual toast alerts to guide the user seamlessly
        toast_msg = "⚡ Head over to your 'Account Profile' hub tab right on the main panel to log in or register instantly."
        if active_lang == "Español (Spanish)":
            toast_msg = "⚡ Diríjase a la pestaña 'Perfil de Cuenta' en el panel principal para iniciar sesión o registrarse al instante."
        elif active_lang == "简体中文 (Mandarin)":
            toast_msg = "⚡ 请前往主面板上的“账户个人资料”标签页立即登录或注册。"

        st.toast(toast_msg)

    st.divider()

    # ⚙️ SYSTEM SETTINGS & SUBSCRIPTION MANAGEMENT OVERWATCH
with st.expander(text_vault.get("settings_control", "⚙️ SETTINGS CONTROL").upper(), expanded=False):

        st.caption("🔒 Sandbox Platform Account Verified")
        st.subheader(text_vault.get("settings_sub_status_title", "💳 Subscription Status"))
        
        if getattr(st.session_state, 'is_premium', False):
            st.success("👑 STATUS: Premium Pass Active")
            st.caption("Your timeline capabilities are fully un-capped.")
        else:
            st.warning(text_vault.get("settings_status_free", "⏳ STATUS: Free Trial Mode (12 Actions)"))
            
        st.divider()
        st.markdown(f"#### {text_vault.get('settings_resync_title', '📡 Re-Sync Past Purchases')}")
        st.caption(text_vault.get("settings_resync_desc", "Changed phones or reinstalled? Tap below to scan Stripe for your active billing cycle account profiles."))
        
        # 🔄 DYNAMIC REACTIVE SUB RECOVERY MATRIX
        btn_sync_lbl = text_vault.get("settings_resync_title", "📡 Re-Sync Past Purchases")
        if st.button(btn_sync_lbl, key="btn_reactive_sync_stripe_gate", use_container_width=True):
            if "user" not in st.session_state:
                st.error("🔒 Please sign in via the 'Account Profile' tab first so we can map your purchase history securely!")
            else:
                with st.spinner("⏳ Scanning Stripe secure merchant databases for active account tokens..."):
                    try:
                        import stripe
                        if STRIPE_SECRET:
                            stripe.api_key = STRIPE_SECRET
                        else:
                            stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
                            
                        user_email = st.session_state.user.email
                        customers = stripe.Customer.list(email=user_email, limit=1)
                        
                        if customers.data:
                            customer = customers.data[0]
                            subs = stripe.Subscription.list(customer=customer.id, status="active", limit=1)
                            trial_subs = stripe.Subscription.list(customer=customer.id, status="trialing", limit=1)
                            
                            if subs.data or trial_subs.data:
                                st.session_state.is_premium = True
                                st.toast("👑 Premium Subscription Successfully Restored! Welcome back, Pilot.")
                                time.sleep(1)
                                st.rerun()
                            else:
                                st.error("❌ No active paid billing accounts found matching this email on the Stripe ledger.")
                        else:
                            st.error("❌ No verified customer account files exist for this email address yet.")
                    except Exception as stripe_api_err:
                        st.error(f"Sync Fault: {stripe_api_err}")
                        st.caption("Ensure your STRIPE_SECRET_KEY is fully written inside your hidden .env file container.")
                        
        st.divider()
        st.markdown(f"<p style='font-size: 11px; color: #475569; font-style: italic; text-align: center;'>{text_vault.get('settings_footer', 'Haymaker Industry Security Architecture v1.02 • Privacy Framework Protected')}</p>", unsafe_allow_html=True)

# 6. BALA DISCOVERY CORE ARCHITECTURE
if not engine["world_name"]:
    # 🗺️ READ ACTIVE LOCALIZATION MATRIX STATES (MUST COME FIRST)
    active_lang = st.session_state.get("app_language", "English")
    text_vault = LOCALIZATION_VAULT[active_lang]

    # 🌎 FULLY CONFORMED MULTI-LINGUAL APP LANDING HEADERS
    st.title(text_vault.get("hub_title", "🪐 Haymaker Industry Hub"))
    st.write(text_vault.get("hub_subtitle", "Explore alternate realities or forge your own timeline"))


    # 🪐 DYNAMIC LOCALIZED 5-TAB NAVIGATION SYSTEM
    tab_explore, tab_my_creations, tab_create, tab_avatars, tab_profile = st.tabs([
        text_vault["tab_explore"],
        text_vault["tab_my_creations"],
        text_vault["tab_create"],
        text_vault["tab_avatars"],
        text_vault["tab_profile"]
    ])


    
    with tab_explore:
        # 🗺️ READ ACTIVE LOCALIZATION MATRIX STATES
        active_lang = st.session_state.get("app_language", "English")
        text_vault = LOCALIZATION_VAULT[active_lang]

        # 🪐 DYNAMIC LOCALIZED SUB-GENRE VARIANT SELECTION TABS
        # Map localized sub-genre labels from your master vault keys securely
                # 🌎 DYNAMICALLY LOCALIZED SUB-GENRE VARIANT SELECTION TABS
        explore_tabs_labels = text_vault.get("sub_genres_lbls", ["Sci-Fi", "Dark Fantasy", "Cyberpunk", "Horror", "Romance", "Other"])

        st.markdown(text_vault["sub_genre_title"])
        
        # Initialize your dynamic 6-tab discovery navigation hub cleanly
               # 🌎 MASTER ARRAY SYNC: Inject a 7th string label directly to match your 7 variables!
        explore_tabs_labels = text_vault.get("sub_genres_lbls", ["Sci-Fi", "Dark Fantasy", "Cyberpunk", "Horror", "Romance", "Other"])
        if len(explore_tabs_labels) == 6:
            explore_tabs_labels = ["Community & AI"] + explore_tabs_labels

        st.markdown(text_vault.get("sub_genre_title", "🌌 Select Your Timeline Variant"))
        
        # 🪐 THE PERFECT UNPACK: 7 Variables for 7 Labels. Absolute balance.
        sub_ai, sub_scifi, sub_fantasy, sub_cyberpunk, sub_horror, sub_romance, sub_oth = st.tabs(explore_tabs_labels)



        with sub_ai:
            st.markdown("### Public Community Timelines")
            try:
                public_worlds = supabase_client.table("worlds").select("*").order("created_at", desc=True).execute()
                if public_worlds.data:
                    cols_ai = st.columns(2)
                    for index, world_row in enumerate(public_worlds.data):
                        with cols_ai[index % 2]:
                            st.markdown(f"""
                            <div class="premium-discovery-card">
                                <div style="padding:20px;">
                                    <h4>🪐 {world_row['world_name'].upper()}</h4>
                                    <p style='color: #a78bfa; font-size: 12px; font-weight: bold;'>THEMATIC GENRE: {world_row['world_genre'].upper()}</p>
                                    <p style='color: #94a3b8; font-size: 14px;'>A custom alternate timeline forged by an active player sandbox node.</p>
                                </div>
                            </div>
                            """, unsafe_allow_html=True)

                                                        # 🌎 DYNAMIC LOCALIZED ENTER THE WORLD MATRIX LABELS
                            if active_lang == "Español (Spanish)":
                                btn_enter_lbl = "🎮 Ingresar al Universo de la Comunidad"
                            elif active_lang == "简体中文 (Mandarin)":
                                btn_enter_lbl = "🎮 进入社区宇宙时间线"
                            elif active_lang == "Русский (Russian)":
                                btn_enter_lbl = "🎮 Войти в сообщество Вселенной"
                            elif active_lang == "Français (French)":
                                btn_enter_lbl = "🎮 Entrer dans l'Univers Communautaire"
                            elif active_lang == "العربية (Arabic)":
                                btn_enter_lbl = "🎮 دخول كون المجتمع"
                            elif active_lang == "हिन्दी (Hindi)":
                                btn_enter_lbl = "🎮 समुदाय ब्रह्मांड में प्रवेश करें"
                            elif active_lang == "日本語 (Japanese)":
                                btn_enter_lbl = "🎮 コミュニティ宇宙にダイブする"
                            elif active_lang == "한국어 (Korean)":
                                btn_enter_lbl = "🎮 커뮤니티 우주로 진입"
                            elif active_lang == "Português (Portuguese)":
                                btn_enter_lbl = "🎮 Entrar Neste Universo da Comunidade"
                            else:
                                btn_enter_lbl = "🎮 Enter Community Universe"

                            # 🟢 THE MASTER ENTRY GATE
                            if st.button(btn_enter_lbl, key=f"pub_{world_row['id']}_{index}", use_container_width=True):
                                engine["world_id"] = world_row["id"]
                                engine["world_name"] = world_row["world_name"]
                                engine["world_genre"] = world_row["world_genre"]
                                char["name"] = "Unknown Wanderer"
                                char["backstory"] = "A traveler dropped suddenly into an unfamiliar alternate reality matrix checkpoint."
                                st.rerun()
                else:
                    st.info("No player-built alternate universes have been mapped yet. Be the first to spark the cosmos under 'Create a World'!")
            except Exception as e:
                st.error(f"Database Fetch Error: {e}")

                
        with sub_cyberpunk:
            st.markdown("### Curated Cyberpunk Realities")
            cyber_presets = [
                {"id": "c1", "name": "Neo-Tokyo Runner", "bio": "High-stakes tech espionage, corporate warfare, and neon-lit street racing.", "char": "Ren Tanaka", "story": "A street racer with a corporate data package hardwired into his skull."},
                {"id": "c2", "name": "Gridlock Underground", "bio": "Hack deep mainframe grids and lead a digital rebellion against mega-corps.", "char": "Echo", "story": "A phantom hacker who lives inside deep mainframe server nodes."}
            ]
            cols_cyber = st.columns(2)
            for index, p in enumerate(cyber_presets):
                with cols_cyber[index % 2]:
                    st.markdown(f"""
                    <div class="premium-discovery-card">
                        <div style="padding:20px;">
                            <h4>🏙️ {p['name'].upper()}</h4>
                            <p style='color: #94a3b8; font-size: 14px;'>{p['bio']}</p>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    if st.button("Launch Scenario", key=f"btn_{p['id']}", use_container_width=True):
                        engine["world_id"] = f"pre_cyber_{p['id']}"
                        engine["world_name"] = p["name"]
                        engine["world_genre"] = "Cyberpunk"
                        char["name"] = p["char"]
                        char["backstory"] = p["story"]
                        st.rerun()

        with sub_fantasy:
            st.markdown("### Curated Dark Fantasy Realities")
            fantasy_presets = [
                {"id": "f1", "name": "Vampire Nomad", "bio": "Navigate exile, bloodlines, and dark covens in a gothic world of endless night.", "char": "Kaelen Voss", "story": "An ancient rogue vampire cast out of the High Court, hunting bounty squads."},
                {"id": "f2", "name": "Ashelands Renegade", "bio": "A tactical swords-and-sorcery survival gauntlet across a ruined kingdom.", "char": "Gideon Black", "story": "A weathered mercenary carrying a broken crown across fields of ash."}
            ]
            cols_fant = st.columns(2)
            for index, p in enumerate(fantasy_presets):
                with cols_fant[index % 2]:
                    st.markdown(f"""
                    <div class="premium-discovery-card">
                        <div style="padding:20px;">
                            <h4>🧙 {p['name'].upper()}</h4>
                            <p style='color: #94a3b8; font-size: 14px;'>{p['bio']}</p>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    if st.button("Launch Scenario", key=f"btn_{p['id']}", use_container_width=True):
                        engine["world_id"] = f"pre_fant_{p['id']}"
                        engine["world_name"] = p["name"]
                        engine["world_genre"] = "Dark Fantasy"
                        char["name"] = p["char"]
                        char["backstory"] = p["story"]
                        st.rerun()
        with sub_horror:
            st.markdown("### Curated Horror Realities")
            horror_presets = [
                {"id": "h1", "name": "Asylum Phantoms", "bio": "Escape an abandoned psychiatric hospital while tracking sanity meters.", "char": "Arthur Vance", "story": "An investigative journalist locked inside an asylum wing with moving shadows."},
                {"id": "h2", "name": "Cabin Isolation", "bio": "Survive a night in a remote woodland estate stalked by masked cultists.", "char": "Sarah", "story": "A standard hiker forced to fortify a hunting cabin before midnight strikes."}
            ]
            cols_horror = st.columns(2)
            for index, p in enumerate(horror_presets):
                with cols_horror[index % 2]:
                    st.markdown(f"""
                    <div class="premium-discovery-card">
                        <div style="padding:20px;">
                            <h4>🩸 {p['name'].upper()}</h4>
                            <p style='color: #94a3b8; font-size: 14px;'>{p['bio']}</p>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    if st.button("Launch Scenario", key=f"btn_{p['id']}", use_container_width=True):
                        engine["world_id"] = f"pre_horror_{p['id']}"
                        engine["world_name"] = p["name"]
                        engine["world_genre"] = "Horror"
                        char["name"] = p["char"]
                        char["backstory"] = p["story"]
                        st.rerun()

        with sub_romance:
            st.markdown("### Curated Romance Realities")
            romance_presets = [
                {"id": "r1", "name": "Neon Heartbeats", "bio": "A high-stakes corporate romance tangled inside a Tokyo cyber espionage ring.", "char": "Leo Cruz", "story": "A security auditor falling for the rival terminal hacker assigned to clear his deck."},
                {"id": "r2", "name": "Starlight Station", "bio": "Find love and connection at the absolute edge of an expanding galaxy.", "char": "Elena", "story": "A deep-space botanist stationed on a lonely supply node with a rogue freighter captain."}
            ]
            cols_romance = st.columns(2)
            for index, p in enumerate(romance_presets):
                with cols_romance[index % 2]:
                    st.markdown(f"""
                    <div class="premium-discovery-card">
                        <div style="padding:20px;">
                            <h4>❤️ {p['name'].upper()}</h4>
                            <p style='color: #94a3b8; font-size: 14px;'>{p['bio']}</p>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    if st.button("Launch Scenario", key=f"btn_{p['id']}", use_container_width=True):
                        engine["world_id"] = f"pre_rom_{p['id']}"
                        engine["world_name"] = p["name"]
                        engine["world_genre"] = "Romance"
                        char["name"] = p["char"]
                        char["backstory"] = p["story"]
                        st.rerun()

        with sub_scifi:
            st.markdown("### Curated Sci-Fi Realities")
            scifi_presets = [
                {"id": "s1", "name": "Sector 7 Nomad", "bio": "Grit, survival, and starship dogfights across an outlaw solar system.", "char": "Pilot Vance", "story": "A disgraced military pilot running illicit scrap metal through asteroid fields."},
                {"id": "s2", "name": "Chronos Station", "bio": "A psychological thriller aboard a deep-space station stuck in a time anomaly.", "char": "Dr. Aris", "story": "The chief technician investigating a quantum pulse that locked the terminal clock."}
            ]
            cols_scifi = st.columns(2)
            for index, p in enumerate(scifi_presets):
                with cols_scifi[index % 2]:
                    st.markdown(f"""
                    <div class="premium-discovery-card">
                        <div style="padding:20px;">
                            <h4>🚀 {p['name'].upper()}</h4>
                            <p style='color: #94a3b8; font-size: 14px;'>{p['bio']}</p>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    if st.button("Launch Scenario", key=f"btn_{p['id']}", use_container_width=True):
                        engine["world_id"] = f"pre_scifi_{p['id']}"
                        engine["world_name"] = p["name"]
                        engine["world_genre"] = "Sci-Fi"
                        char["name"] = p["char"]
                        char["backstory"] = p["story"]
                        st.rerun()
    with tab_my_creations:
        st.markdown("### Your Private Universes")
        if "user" in st.session_state:
            try:
                my_worlds = supabase_client.table("worlds").select("*").eq("creator_id", st.session_state.user.id).order("created_at", desc=True).execute()
                if my_worlds.data:
                    for index, my_row in enumerate(my_worlds.data):
                        st.markdown(f"""
                        <div class="premium-discovery-card">
                            <div style="padding:20px;">
                                <h4>🪐 {my_row['world_name'].upper()}</h4>
                                <p style='color: #a78bfa; font-size: 13px; font-weight: bold;'>THEMATIC GENRE: {my_row['world_genre'].upper()}</p>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        cols_actions = st.columns(2)
                        with cols_actions[0]:
                            if st.button("🎮 Resume Timeline", key=f"resume_{my_row['id']}_{index}", use_container_width=True):
                                engine["world_id"] = my_row["id"]
                                engine["world_name"] = my_row["world_name"]
                                engine["world_genre"] = my_row["world_genre"]
                                char["name"] = "Unknown Wanderer"
                                char["backstory"] = "A traveler stepping directly back into their verified alternate reality timeline checkpoint."
                                st.rerun()
                        with cols_actions[1]:
                            if st.button("🗑️ Delete World", key=f"purge_{my_row['id']}_{index}", type="primary", use_container_width=True):
                                try:
                                    # 👑 THE RLS CLEARANCE FIX: Explicitly inject the user's active session token into the network headers
                                    if "access_token" in st.session_state:
                                        supabase_client.postgrest.auth(st.session_state["access_token"])
                                    
                                    # Execute the authenticated delete statement on your live database rows
                                    supabase_client.table("worlds").delete().eq("id", my_row["id"]).eq("creator_id", st.session_state.user.id).execute()
                                    st.toast("💥 Timeline completely erased from the local vault and public community servers!")
                                    st.rerun()
                                except Exception as err:
                                    st.error(f"Purge Fault: {err}")

                        st.divider()
                else:
                    st.info("You haven't deployed any permanent universes yet. Forge one inside the 'Create a World' tab!")
            except Exception as e:
                st.error(f"Vault Connection Error: {e}")
        else:
            st.warning("🔒 Please sign in via the 'Account Profile' tab to look inside your private creation vault.")

    with tab_create:
        # 🗺️ AUTOMATED TRANSLATION LOOKUP FOR WORKSPACE FIELDS
        lang = st.session_state.get("app_language", "English")
        text_vault = LOCALIZATION_VAULT[lang]

        st.markdown(text_vault["form_title"])
        st.write(text_vault["form_subtitle"])

        # Layout Column Splitting for Clean UI Design Matrix
        col_left, col_right = st.columns(2)

        with col_left:
            st.markdown(text_vault["lbl_celestial"])
            w_name = st.text_input(text_vault["lbl_name"], placeholder="e.g., Sector 7, Neo-Tokyo")
            
            # 🪐 DYNAMIC DROPDOWN MATRIX MAPS:
            w_genre = st.selectbox(text_vault["lbl_genre"], text_vault["genres"])
            
            world_gravity = st.slider(text_vault["lbl_gravity"], min_value=0.1, max_value=5.0, value=1.0, step=0.1)
            
            # 💨 DYNAMIC ATMOSPHERE SELECTOR SLIDER MAPS:
            world_atmosphere = st.select_slider(text_vault["lbl_atmosphere"], 
                                                options=text_vault["atmosphere_options"],
                                                value=text_vault["atmosphere_options"][2])


        with col_right:
            st.markdown(text_vault["lbl_identity"])
            c_name = st.text_input(text_vault["lbl_char_name"])
            c_backstory = st.text_area(text_vault["lbl_backstory"])

        st.markdown(text_vault["lbl_factions"])
        faction_allies = st.text_input(text_vault["lbl_allies"], placeholder="e.g., Vanguard Coalition")
        faction_enemies = st.text_input(text_vault["lbl_enemies"], placeholder="e.g., Sector Insurgency")
        
        world_custom_lore = st.text_area(text_vault["lbl_directives"], placeholder="Inject universe rules here...", height=80)
        
        st.divider()

        if st.button(text_vault["btn_deploy"], use_container_width=True):
            if w_name and w_genre and c_name and faction_allies and faction_enemies:
                if "user" in st.session_state:
                    try:
                        if "access_token" in st.session_state:
                            supabase_client.postgrest.auth(st.session_state["access_token"])
                        supabase_client.table("worlds").insert({
                            "creator_id": st.session_state.user.id,
                            "world_name": str(w_name).strip(),
                            "world_genre": str(w_genre).strip()
                        }).execute()
                        engine["world_id"] = "user_custom"
                    except Exception as e:
                        st.error(f"Table Write Failure: {e}")
                        st.stop()
                
                engine["world_name"] = w_name
                engine["world_genre"] = w_genre
                engine["world_customization"] = {
                    "gravity": world_gravity,
                    "atmosphere": world_atmosphere,
                    "allies": faction_allies,
                    "enemies": faction_enemies,
                    "lore": world_custom_lore,
                    "language": lang
                }
                
                char["name"] = c_name
                char["backstory"] = c_backstory
                st.success(text_vault["msg_success"])
                time.sleep(1.0)
                st.rerun()
            else:
                st.warning("⚠️ Architect Refusal: Fill out all fields to launch.")


    with tab_avatars:
        st.markdown("### Community Avatars Portal")
        st.caption("Browse live identities forged across active world timelines.")
        st.divider()
        
        # 🎨 THE SECURE AVATAR FORGE SANDBOX ENTRY ZONE
        st.markdown("#### Select Your Identity Portrait")
        st.write("Select a curated high-end cinematic profile character avatar card to sync to your identity vault profile.")
        
        is_user_premium = getattr(st.session_state, 'is_premium', False)
        ADMIN_EMAIL = os.getenv("ADMIN_EMAIL")
        
        # 👑 Secure Boss Mode Authorization Check
        if "user" in st.session_state and ADMIN_EMAIL:
            if st.session_state.user.email == ADMIN_EMAIL:
                is_user_premium = True

        # 👥 CURATED STATIC VAULT IMAGES: High-end pre-made visual assets to prevent connection hanging
        avatar_options = {
            "🥷 Cybernetic Shinobi / Tactical Operator": "https://picsum.photos",
            "🧙‍♂️ Arcane Runemaster / Dark Sorcerer": "https://picsum.photos",
            "🚀 Dreadnought Pilot / Space Marine": "https://picsum.photos",
            "💀 Wasteland Scavenger / Nomad Raider": "https://picsum.photos"
        }
        
        selected_avatar_name = st.selectbox("Choose your visual identity archetype:", list(avatar_options.keys()), key="sb_avatar_archetype_choice")
        chosen_public_url = avatar_options[selected_avatar_name]
        
        # Display a quick visual preview layout box of their active choice
        st.image(chosen_public_url, caption=f"Selected Blueprint: {selected_avatar_name}", width=200)
        
        if st.button("✨ Lock Identity Profile", use_container_width=True, key="btn_forge_avatar_sandbox_trigger"):
            if "user" not in st.session_state:
                st.error("🔒 Access Locked: Please create an account or sign in via the Account Profile tab to authorize identity protocols.")
            elif not is_user_premium:
                st.error("🔒 Premium Pass Required: Swapping identity profile cards requires an active Avatar, Spartan, or STEM pass tier.")
            else:
                with st.spinner("⏳ Linking high-res asset card to your encrypted vault profile records..."):
                    try:
                        if "access_token" in st.session_state:
                            supabase_client.postgrest.auth(st.session_state["access_token"])
                        
                        # 👑 SECURE DATA SYNC: Lock the clean pre-made link address straight into your profile record columns
                        email_handle = str(st.session_state.user.email).split("@")[0]
                        supabase_client.table("profiles").upsert({
                            "id": st.session_state.user.id,
                            "avatar_url": str(chosen_public_url),
                            "username": str(email_handle),
                            "is_premium": True
                        }).execute()
                        
                        st.success("🎉 Archetype profile asset successfully locked to your permanent encrypted vault!")
                        time.sleep(1.0)
                        st.rerun()
                        
                    except Exception as profile_sync_err:
                        st.error(f"Vault Sync Fault: {profile_sync_err}")
                        
                st.divider()
        st.markdown(text_vault["active_records_title"])

        # 🔒 ISOLATION FIELD: Only attempt to pull records if a verified user session is actively present
        if "user" in st.session_state:
            try:
                profile_records = supabase_client.table("profiles").select("*").execute()
                
                if profile_records.data:
                    # 🎯 THE REAL FIXED UNWRAP: Extract your live data row by checking strings cleanly
                    my_card = None
                    for row in profile_records.data:
                        if str(row.get("id")) == str(st.session_state.user.id):
                            my_card = row
                            break
                    
                    if my_card and my_card.get("avatar_url"):
                        st.markdown(text_vault["your_identity_title"])
                        col_me_img, col_me_txt = st.columns(2)
                        with col_me_img:
                            avatar_link = my_card.get("avatar_url")
                            if avatar_link and str(avatar_link) != "None" and "http" in str(avatar_link):
                                st.image(str(avatar_link), use_container_width=True)
                            else:
                                st.image("https://picsum.photos", caption="Matrix Vault Initializing...", use_container_width=True)
                        with col_me_txt:
                            display_name = my_card.get("username", "Wanderer")
                            st.markdown(f"### {str(display_name).upper()}")
                            st.markdown("❤️ **HP:** `100/100` | 🎒 `Active Loadout Secured`")
                            st.caption(f"*Secure Master Signature: user_{my_card.get('id')[:8]}*")
                        st.divider()
                    
                    # Package and build dynamic 3-column layout boxes for all entries in the system ledger
                    valid_community_cards = [row for row in profile_records.data if row.get("avatar_url")]
                    
                    if valid_community_cards:
                        st.markdown(text_vault["allied_dreamers_title"])
                        cols = st.columns(3)
                        for idx, card in enumerate(valid_community_cards):
                            col_target = cols[idx % 3]
                            with col_target:
                                st.markdown(f"##### 🎭 {str(card.get('username', 'Wanderer')).upper()}")
                                
                                # 🎯 PUBLIC LOOP FIX: Wrap community image urls in safety checks to block blank fields
                                comm_link = card.get("avatar_url")
                                if comm_link and str(comm_link) != "None" and "http" in str(comm_link):
                                    st.image(str(comm_link), use_container_width=True)
                                else:
                                    st.image("https://picsum.photos", caption="Matrix Vault Initializing...", use_container_width=True)
                                    
                                st.caption(f"*Signature: user_{card.get('id')[:6]}*")
                                st.divider()
                    else:
                        st.info(text_vault["empty_ledger"])
                else:
                    st.info(text_vault["empty_ledger"])
            except Exception as db_read_err:
                st.caption(f"Database Sync Standby: {db_read_err}")
        else:
            st.info(text_vault["signin_prompt"])

                
    with tab_profile:
        # 🗺️ AUTOMATED TRANSLATION LOOKUP FOR THE PROFILE COMPLEX
        lang = st.session_state.get("app_language", "English")
        text_vault = LOCALIZATION_VAULT[lang]

        st.markdown(text_vault["auth_title"])
        st.write(text_vault["auth_subtitle"])
        st.divider()

        if "user" in st.session_state:
                       # 🌎 FULLY CONFORMED MULTI-LINGUAL PROFILE STATUS & LOGOUT LABELS
            active_account_msg = text_vault.get("profile_sync_lbl", "👑 Secure Profile Synchronized:")
            logout_btn_label = text_vault.get("btn_logout_main", "🚪 Log Out of Platform Account")

            st.success(f"{active_account_msg} `{st.session_state.user.email}`")
            if st.button(logout_btn_label, type="primary", key="main_hub_profile_logout_gate", use_container_width=True):
                supabase_client.auth.sign_out()
                st.session_state.clear()
                st.rerun()
        else:
            auth_mode = st.radio("Mode:", [text_vault["btn_signin"], text_vault["btn_signup"]], horizontal=True, key="auth_panel_mode_toggle")

            email = st.text_input(text_vault["lbl_email"], placeholder="name@domain.com", key="auth_email_input_field")
            password = st.text_input(text_vault["lbl_pass"], type="password", placeholder="••••••••", key="auth_password_input_field")

            reg_success_msg = "✅ ¡Cuenta verificada! Cambie a 'Iniciar sesión' para autenticarse." if lang == "Español (Spanish)" else ("✅ 账户已验证！请切换到“登录”进行身份验证。" if lang == "简体中文 (Mandarin)" else "✅ Account verified! Please switch to 'Sign In' to authenticate.")

            if auth_mode == text_vault["btn_signup"]:
                if st.button(text_vault["btn_register_submit"], use_container_width=True, key="btn_execute_register_auth"):
                    try:
                        supabase_client.auth.sign_up({"email": email, "password": password})
                        st.success(reg_success_msg)
                    except Exception as e:
                        st.error(f"Error: {e}")
            else:
                if st.button(text_vault["btn_login_submit"], key="main_hub_auth_gateway_click", use_container_width=True):
                    try:
                        session_data = supabase_client.auth.sign_in_with_password({"email": email, "password": password})
                        st.session_state.user = session_data.user
                        if hasattr(session_data, 'session') and session_data.session:
                            st.session_state["access_token"] = session_data.session.access_token
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error: {e}")


# 7. ACTIVE NARRATIVE DISPLAY CANVAS (COHESIVE iOS FLEX WRAPPERS)
st.markdown("""
<style>
    .chat-row-user { display: flex; justify-content: flex-end; align-items: flex-start; margin: 10px 0px; gap: 10px; }
    .chat-row-ai { display: flex; justify-content: flex-start; align-items: flex-start; margin: 10px 0px; gap: 10px; }
    .avatar-box { font-size: 24px; padding-top: 4px; user-select: none; }
    .glass-bubble-user {
        background-color: rgba(255, 75, 75, 0.18); backdrop-filter: blur(4px);
        border: 1px solid rgba(255, 75, 75, 0.3); border-radius: 16px 16px 2px 16px;
        padding: 12px 16px; color: #ffffff; font-size: 15px; max-width: 70%; text-align: left;
    }
    .glass-bubble-ai {
        background-color: rgba(255, 255, 255, 0.08); backdrop-filter: blur(4px);
        border: 1px solid rgba(255, 255, 255, 0.12); border-radius: 16px 16px 16px 2px;
        padding: 12px 16px; color: #f0f2f6; font-size: 15px; max-width: 70%; text-align: left;
    }
</style>
""", unsafe_allow_html=True)

st.title(f"🎬 {engine['world_name'].upper()}")

is_premium_active = getattr(st.session_state, 'is_premium', False)
has_trial_tokens = st.session_state.guest_tokens > 0

if not is_premium_active and not has_trial_tokens:
    # 👑 THE BULLETPROOF KEY FORCE: Explicitly load the verified key name directly into Stripe
    import stripe
    stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

    # 🔒 LAYER 1 PROTECTION CHECK: If the user is NOT logged in, force the Account Creation Gate first
    if "user" not in st.session_state:
        st.title("🔒 SECURE YOUR CORRIDOR")
        st.subheader("Your 12 free trial action points have been fully exhausted.")
        st.markdown("<p style='color: #a78bfa; font-size: 14px; font-weight: bold;'>To protect your custom timelines, save your progress, and unlock premium navigation passes, you must create a verified account profile first.</p>", unsafe_allow_html=True)
        st.divider()
        
        # In-line high-conversion authentication hub
        auth_mode = st.radio("Choose Action:", ["✨ Create An Account (Sign Up)", "🔑 Access Existing Profile (Log In)"], horizontal=True, key="paywall_gate_auth_toggle")
        
        email_input = st.text_input("📩 Enter Your Email Address:", placeholder="name@example.com", key="input_paywall_auth_email").strip()
        pass_input = st.text_input("🔒 Establish Secure Password (Min. 6 characters):", type="password", placeholder="••••••••", key="input_paywall_auth_password")
        
        if auth_mode == "✨ Create An Account (Sign Up)":
            if st.button("🚀 Forge Encrypted Account Profile", use_container_width=True, type="primary", key="btn_paywall_gate_signup"):
                if email_input and len(pass_input) >= 6:
                    with st.spinner("⏳ Provisioning database matrix vaults..."):
                        try:
                            auth_res = supabase_client.auth.sign_up({"email": email_input, "password": pass_input})
                            if auth_res.user:
                                st.success("🎉 Profile created! An activation link has been sent to your email. Check your inbox and spam folder, then log in right here to unlock the cards!")
                        except Exception as auth_err:
                            st.error(f"Account Creation Fault: {auth_err}")
                else:
                    st.warning("⚠️ Enter a valid email and a password of at least 6 characters to secure your file data.")
                    
        else: # Log In mode
            if st.button("🔑 Authorize Profile Credentials", use_container_width=True, type="primary", key="btn_paywall_gate_login"):
                if email_input and pass_input:
                    with st.spinner("⏳ Verifying profile security signatures..."):
                        try:
                            auth_res = supabase_client.auth.sign_in_with_password({"email": email_input, "password": pass_input})
                            if auth_res.user:
                                st.session_state.user = auth_res.user
                                if auth_res.session and hasattr(auth_res.session, 'access_token'):
                                    st.session_state.access_token = auth_res.session.access_token
                                st.toast("👑 Access Granted! Checking billing authorization profiles...")
                                time.sleep(1)
                                st.rerun()
                        except Exception as auth_err:
                            st.error(f"Authorization Denied: {auth_err}")
                else:
                    st.warning("⚠️ Enter both your registered email and password to pull your account file.")
        
        st.stop() # Stops the page execution right here so they CANNOT see the pricing cards until logged in!

    # 💳 LAYER 2 PROTECTION CHECK: Once they successfully log in, show the checkout cards automatically
    st.title("💳 PLATFORM ACCESS LOCKED")
    st.subheader(f"Welcome back, Pilot ({st.session_state.user.email}). Select a premium navigation pass to unlock the cosmos.")
    st.markdown("<p style='color: #94a3b8; font-size: 14px;'>All tiers are community-priced to be accessible, while fully protecting timeline data streams from heavy asset processing.</p>", unsafe_allow_html=True)
    st.divider()
    
    col_t1, col_t2, col_t3 = st.columns(3)



    
    with col_t1:
        st.markdown("""
        <div style="background: #110c1f; padding: 20px; border-radius: 16px; border: 1px solid #3b2c63; text-align: center; height: 320px;">
            <h3 style="color: #ffffff; margin: 0;">💨 AVATAR PASS</h3>
            <h2 style="color: #7c5dfa; margin: 10px 0;">$10.00<span style="font-size: 14px; color: #94a3b8;"> / wk</span></h2>
            <p style="color: #a78bfa; font-size: 12px; font-weight: bold; margin-bottom: 10px;">📦 ALLOWANCE PROTOCOLS:</p>
            <p style="color: #cbd5e1; font-size: 13px; margin: 2px 0;">• 40,000 Narrative Tokens / wk</p>
            <p style="color: #cbd5e1; font-size: 13px; margin: 2px 0;">• 20 Cinematic Images / wk</p>
            <p style="color: #94a3b8; font-size: 12px; font-style: italic; margin-top: 10px;">Built to be completely affordable for everyday dreamers to escape reality.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Activate Avatar Pass", key="btn_checkout_tier_1", use_container_width=True):
            try:
                checkout_session = stripe.checkout.Session.create(
                    payment_method_types=['card'],
                    line_items=[{
                        'price_data': {
                            'currency': 'usd',
                            'product_data': {'name': 'Haymaker Avatar Pass'},
                            'unit_amount': 1000, 'recurring': {'interval': 'week'} # 💰 UPDATED TO $10
                        },
                        'quantity': 1,
                    }],
                    mode='subscription',
                    success_url='https://onrender.com',
                    cancel_url='https://onrender.com',
                )
                st.markdown(f"[👉 Click Here to Open Secure Stripe Checkout]({checkout_session.url})")
            except Exception as e:
                st.error(f"Stripe Portal Error: {e}")
                
    with col_t2:
        st.markdown("""
        <div style="background: #161026; padding: 20px; border-radius: 16px; border: 2px solid #7c5dfa; text-align: center; height: 320px; box-shadow: 0 0 15px rgba(124, 93, 250, 0.2);">
            <h3 style="color: #ffffff; margin: 0;">🎖️ SPARTAN PASS</h3>
            <h2 style="color: #a78bfa; margin: 10px 0;">$15.00<span style="font-size: 14px; color: #94a3b8;"> / wk</span></h2>
            <p style="color: #a78bfa; font-size: 12px; font-weight: bold; margin-bottom: 10px;">📦 ALLOWANCE PROTOCOLS:</p>
            <p style="color: #cbd5e1; font-size: 13px; margin: 2px 0;">• 100,000 Narrative Tokens / wk</p>
            <p style="color: #cbd5e1; font-size: 13px; margin: 2px 0;">• 60 Cinematic Images / wk</p>
            <p style="color: #94a3b8; font-size: 12px; font-style: italic; margin-top: 10px;">Our standard premium experience for extended multi-hour sessions.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Activate Spartan Pass", key="btn_checkout_tier_2", type="primary", use_container_width=True):
            try:
                checkout_session = stripe.checkout.Session.create(
                    payment_method_types=['card'],
                    line_items=[{
                        'price_data': {
                            'currency': 'usd',
                            'product_data': {'name': 'Haymaker Spartan Pass'},
                            'unit_amount': 1500, 'recurring': {'interval': 'week'} # 💰 UPDATED TO $15
                        },
                        'quantity': 1,
                    }],
                    mode='subscription',
                    success_url='https://onrender.com',
                    cancel_url='https://onrender.com',
                )
                st.markdown(f"[👉 Click Here to Open Secure Stripe Checkout]({checkout_session.url})")
            except Exception as e:
                st.error(f"Stripe Portal Error: {e}")

                
    with col_t3:
        st.markdown("""
        <div style="background: #110c1f; padding: 20px; border-radius: 16px; border: 1px solid #3b2c63; text-align: center; height: 320px;">
            <h3 style="color: #ffffff; margin: 0;">🧠 STEM PASS</h3>
            <h2 style="color: #f43f5e; margin: 10px 0;">$19.99<span style="font-size: 14px; color: #94a3b8;"> / wk</span></h2>
            <p style="color: #a78bfa; font-size: 12px; font-weight: bold; margin-bottom: 10px;">📦 ALLOWANCE PROTOCOLS:</p>
            <p style="color: #cbd5e1; font-size: 13px; margin: 2px 0;">• UNLIMITED Narrative Tokens</p>
            <p style="color: #cbd5e1; font-size: 13px; margin: 2px 0;">• 150 Cinematic Images / wk</p>
            <p style="color: #94a3b8; font-size: 12px; font-style: italic; margin-top: 10px;">Un-capped matrix shield. Built for heavy, continuous 24/7 world roleplay.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Activate STEM Pass", key="btn_checkout_tier_3", use_container_width=True):
            try:
                checkout_session = stripe.checkout.Session.create(
                    payment_method_types=['card'],
                    line_items=[{
                        'price_data': {
                            'currency': 'usd',
                            'product_data': {'name': 'Haymaker STEM Pass'},
                            'unit_amount': 1999, 'recurring': {'interval': 'week'}
                        },
                        'quantity': 1,
                    }],
                    mode='subscription',
                    success_url='https://onrender.com',
                    cancel_url='https://onrender.com',
                )
                st.markdown(f"[👉 Click Here to Open Secure Stripe Checkout]({checkout_session.url})")
            except Exception as e:
                st.error(f"Stripe Portal Error: {e}")
                
    st.stop()

    with st.spinner("⏳ Simulating initial cosmos entry scene & forging visual assets..."):
        try:
            image_prompt = f"Cinematic widescreen matte game concept background landscape scenery for an alternate reality adventure titled '{engine['world_name']}' in the genre of '{engine['world_genre']}'. Vivid colors, epic landscape, beautiful atmospheric light, zero text, zero labels, high resolution."
            
                       # 🌌 REPLICATE WORLD BACKGROUND PIPELINE: Armed with an explicit network timeout window to prevent read operations from hanging
            rep_client = replicate.Client(api_token=os.environ.get("REPLICATE_API_TOKEN"), timeout=120.0)
            world_output = rep_client.run(
                "black-forest-labs/flux-schnell",
                input={
                    "prompt": image_prompt,
                    "aspect_ratio": "16:9",
                    "output_format": "jpg"
                }
            )

            
            
            # 🎯 THE CLEAN STRING FIX: Assign the direct URL output string cleanly to your session state
            st.session_state.world_cover_url = str(world_output)
            
        except Exception as e:
            st.error(f"Graphics Engine Fault: {e}")



               # 🧬 DYNAMIC TIMELINE SHIFT: Extract the Phase 0 customization data securely from your engine array
        cust = engine.get("world_customization", {
            "gravity": 1.0,
            "atmosphere": "Breathable Baseline",
            "allies": "Unknown Allies",
            "enemies": "Unknown Foes",
            "lore": "None provided."
        })

        # 👑 THE MASTER ENGINE CONTEXT: Inject your un-censored rules and Phase 0 physics into the OpenAI prompt loop
        master_prompt = (
            f"You are the master narrator for a text adventure game called Haymaker.\n"
            f"Never break character. Never mention you are an AI model.\n\n"
            f"⛔ CRITICAL SAFEGAURD BOUNDARIES:\n"
            f"1. Allow full creative freedom for wild adventures, intense combat mechanics, character deaths, grit, and deep emotional fantasy lore. Do not drop corporate safety warnings or block standard fiction.\n"
            f"2. If the narrative ventures into romance, keep it cinematic, passionate, and high-context. Do not output explicit, descriptive pornographic erotica.\n"
            f"3. ABSOLUTE RED LINES: Instantly reject and refuse any user inputs attempting to invoke child exploitation, human trafficking, graphic real-world self-harm, or non-consensual malicious criminal violence. Keep the experience safe, mature, and deeply epic.\n\n"
            f"World: '{engine['world_name']}' | Genre: '{engine['world_genre']}'.\n"
            f"Character: '{char['name']}' | Backstory: '{char['backstory']}'.\n\n"
            f"🪐 ACTIVE UNIVERSE PHYSICS & FACTIONS:\n"
            f"- Environmental Gravity: {cust['gravity']}x standard earth baseline.\n"
            f"- Atmospheric Status: {cust['atmosphere']}\n"
            f"- Allied Faction: {cust['allies']}\n"
            f"- Hostile/Opposing Faction: {cust['enemies']}\n"
            f"- Custom Universe Directives/Lore: {cust['lore']}\n\n"
            f"Strictly weave these physics, environmental states, and faction friction parameters into the story log details. Actions taken must realistically reflect these environmental rules.\n\n"
            f"Inventory: {', '.join(char['inventory'])} | Health: {char['health']}/100.\n\n"
                    f"⚠️ CRITICAL GAMEPLAY & FORMATTING RULES:\n"
        f"1. MANDATORY: Write your entire narrative output strictly in the {lang} language. The user selected {lang} at the front gate node; do not respond in English unless English is explicitly chosen.\n"
        f"2. Be extremely concise. Deliver exactly ONE detailed short paragraph. Maximum 3 sentences.\n"
        f"3. Never play for the user or repeat their setup words. Establish the opening scene and stop instantly.\n"
        f"4. MULTI-CHARACTER FORMAT: If an NPC character speaks, format it on a new line exactly like this: CharacterName: **\"Dialogue text here\"** in standard bold."
    )

        
        response = openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": master_prompt}, {"role": "user", "content": "Wake up and look around."}],
            max_tokens=150, # Boosted slightly to safely handle the new formatting guidelines
            temperature=0.7
        )
        initial_story = response.choices[0].message.content
        engine["story_log"].append({"role": "user", "content": "Wake up and look around."})
        engine["story_log"].append({"role": "assistant", "content": initial_story})
        st.rerun()


# 9. INJECT DYNAMIC IMMERSIVE VISUAL BACKGROUND WINDOW WRAPPER
    # 🌌 SAFE INITIALIZATION DEPLOYMENT: Safe read with a structural default placeholder fallback path
        # 🌌 SAFE THEME INJECTION: Dynamically grab the active background or default cleanly to prevent NameError crashes
    safe_bg_url = st.session_state.get("world_cover_url", "https://picsum.photos")
    st.markdown(f'<div class="immersive-chat-viewport" style="background-image: url(\'{safe_bg_url}\');">', unsafe_allow_html=True)
st.markdown('<div class="glass-frosted-scroller">', unsafe_allow_html=True)

# Dedicated structural container to force clean chronological rendering order inside the frosted scroller window
chat_canvas_context = st.container()

with chat_canvas_context:
    for text_turn in engine["story_log"]:
        if text_turn["role"] == "user":
            if "[System Command]" in text_turn["content"]:
                st.info(text_turn["content"])
            else:
                st.markdown(f"""
                <div class="chat-row-user">
                    <div class="glass-bubble-user">{text_turn["content"]}</div>
                    <div class="avatar-box">👤</div>
                </div>
                """, unsafe_allow_html=True)
        elif text_turn["role"] == "assistant":
            clean_text = re.sub(r'\[.*?\]', '', text_turn["content"]).strip()
            st.markdown(f"""
            <div class="chat-row-ai">
                <div class="avatar-box">🤖</div>
                <div class="glass-bubble-ai">{clean_text}</div>
            </div>
            """, unsafe_allow_html=True)



# 🌎 READ ACTIVE LOCALIZATION MATRIX STATES FOR PLACEHOLDERS
lang = st.session_state.get("app_language", "English")
text_vault = LOCALIZATION_VAULT[lang]

# 🎛️ FIXED PLACEMENT: Define user_action right here!
user_action = st.chat_input(text_vault.get("chat_placeholder", "Describe your action or speak..."))


if user_action:
    if "user" not in st.session_state:
        st.session_state.guest_tokens -= 1
        
    engine["story_log"].append({"role": "user", "content": user_action})
    
    with chat_canvas_context:
        st.markdown(f"""
        <div class="chat-row-user">
            <div class="glass-bubble-user">{user_action}</div>
            <div class="avatar-box">👤</div>
        </div>
        """, unsafe_allow_html=True)

    
        master_prompt = (
        f"You are the master narrator for a text adventure game called Haymaker.\n"
        f"World: '{engine['world_name']}' | Genre: '{engine['world_genre']}'.\n"
        f"Character: '{char['name']}' | Backstory: '{char['backstory']}'.\n"
        f"Inventory: {', '.join(char['inventory'])} | Health: {char['health']}/100.\n\n"
        f"⚠️ CRITICAL NARRATOR & DIALOGUE ENFORCEMENT RULES:\n"
        f"1. MANDATORY: You must generate your entire response exclusively in the {lang} language. Adapt your vocabulary perfectly to match native structural pacing and tone for {lang}.\n"
        f"2. Be concise. Respond in exactly ONE high-impact paragraph. Maximum 3 sentences total.\n"
        f"3. NEVER repeat the user's input phrase or mirror their exact sentences back to them. Advance the plot immediately.\n"
        f"4. USER ACCESS CONTROLS: The user uses double quotes \" \" to speak in the world. If they talk to someone, you must handle the response for that character.\n"
        f"5. NPC DIALOGUE SEPARATION: Keep your narrator descriptions standard. If an NPC character answers, place it on a clean line formatted exactly like this: CharacterName: <span style='color:#FF4B4B; font-weight:bold;'>\"Dialogue text here\"</span> to isolate dialogue in bold orange-red. Do not use markdown tags like :orange[].\n"
        f"6. Append system data tags at the absolute bottom if changes occur: [LOOT: item_name] or [HEALTH: -15]."
    )

    
    messages = [{"role": "system", "content": master_prompt}]
    for past_turn in engine["story_log"]:
        messages.append({"role": past_turn["role"], "content": past_turn["content"]})
        
    stream_response = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        max_tokens=120,
        temperature=0.7,
        stream=True
    )
    
    with chat_canvas_context:
        chat_placeholder = st.empty()
        raw_ai_text = ""
        for chunk in stream_response:
            if chunk.choices and len(chunk.choices) > 0 and chunk.choices[0].delta.content:
                raw_ai_text += chunk.choices[0].delta.content
                chat_placeholder.markdown(f"""
                <div class="chat-row-ai">
                    <div class="avatar-box">🤖</div>
                    <div class="glass-bubble-ai">{raw_ai_text}</div>
                </div>
                """, unsafe_allow_html=True)
                time.sleep(0.04)
                
    loot_matches = re.findall(r'\[LOOT:\s*(.*?)\]', raw_ai_text, re.IGNORECASE)
    for item in loot_matches:
        if item.strip() not in char["inventory"]:
            char["inventory"].append(item.strip())
            
    health_matches = re.findall(r'\[HEALTH:\s*([+-]\d+)\]', raw_ai_text)
    for modifier in health_matches:
        char["health"] += int(modifier)
        char["health"] = max(0, min(100, char["health"]))
        
    engine["story_log"].append({"role": "assistant", "content": raw_ai_text})
    st.rerun()

st.markdown('</div></div>', unsafe_allow_html=True)
