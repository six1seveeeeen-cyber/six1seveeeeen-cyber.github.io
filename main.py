import http.server
import socketserver

PORT = 5000

HTML_PAGE = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Для мамы</title>
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@1,600&family=Montserrat:wght@300;400&display=swap" rel="stylesheet">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body {
            background: #0a0a0a;
            color: white;
            font-family: 'Montserrat', sans-serif;
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            transition: background 2s ease;
            padding: 20px;
        }

        /* Экран ввода */
        .input-screen {
            text-align: center;
            z-index: 10;
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 20px;
            transition: opacity 0.8s ease;
        }

        .input-screen h2 {
            font-size: 1.2rem;
            color: #ffb6c1;
            font-weight: 300;
            letter-spacing: 1px;
            text-shadow: 0 0 10px rgba(255, 182, 193, 0.5);
            line-height: 1.5;
        }

        /* Красивое поле ввода */
        input {
            background: rgba(255, 255, 255, 0.05);
            border: 2px solid rgba(255, 182, 193, 0.3);
            border-radius: 50px;
            padding: 15px 30px;
            font-size: 1.2rem;
            color: white;
            text-align: center;
            outline: none;
            font-family: 'Montserrat', sans-serif;
            transition: all 0.3s ease;
            width: 80vw;
            max-width: 300px;
            box-shadow: 0 0 20px rgba(255, 182, 193, 0.1);
        }

        input:focus {
            border-color: #ffb6c1;
            box-shadow: 0 0 30px rgba(255, 182, 193, 0.4);
            background: rgba(255, 255, 255, 0.1);
        }

        input::placeholder { color: transparent; }

        /* Кнопка */
        button {
            background: linear-gradient(45deg, #ff9a9e, #fecfef);
            border: none;
            border-radius: 50px;
            padding: 15px 40px;
            font-size: 1.1rem;
            color: #333;
            font-weight: bold;
            cursor: pointer;
            transition: transform 0.2s, box-shadow 0.2s;
            box-shadow: 0 5px 15px rgba(255, 105, 180, 0.3);
        }

        button:hover { transform: scale(1.05); box-shadow: 0 8px 25px rgba(255, 105, 180, 0.6); }

        /* Скрытый контент */
        .secret-content {
            display: none;
            text-align: center;
            z-index: 10;
            max-width: 90vw;
            padding: 40px 25px;
            background: rgba(20, 10, 20, 0.6);
            backdrop-filter: blur(15px);
            border-radius: 25px;
            border: 1px solid rgba(255, 182, 193, 0.3);
            box-shadow: 0 0 60px rgba(255, 105, 180, 0.3);
            opacity: 0;
            transition: opacity 1s ease;
        }

        .secret-content h1 {
            font-family: 'Playfair Display', serif;
            font-size: 2.2rem;
            background: linear-gradient(to right, #ff9a9e 0%, #fecfef 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 15px;
            transform: translateY(-20px);
            animation: fade-down 1s forwards 0.5s;
        }

        .secret-content h3 {
            font-size: 0.9rem;
            color: #ffb6c1;
            margin-bottom: 25px;
            letter-spacing: 2px;
            text-transform: uppercase;
            opacity: 0;
            animation: fade-in 1s forwards 1s;
        }

        .secret-content p.main-text {
            font-family: 'Playfair Display', serif;
            font-style: italic;
            font-size: 1.15rem;
            line-height: 1.7;
            color: #f8f8f8;
            margin-bottom: 25px;
            opacity: 0;
            animation: fade-in 2s forwards 2s;
            text-shadow: 0 0 10px rgba(255, 255, 255, 0.2);
            text-align: left;
        }

        .secret-content p.thanks {
            font-size: 0.95rem;
            color: #ffb6c1;
            line-height: 1.5;
            opacity: 0;
            animation: fade-in 1s forwards 3.5s;
            font-weight: bold;
        }

        @keyframes fade-down { to { opacity: 1; transform: translateY(0); } }
        @keyframes fade-in { to { opacity: 1; } }

        /* Падающие сердечки в стиле iOS */
        .heart {
            position: fixed;
            top: -10vh;
            user-select: none;
            pointer-events: none;
            animation: fall linear forwards;
            z-index: 1;
        }

        .heart-shape {
            position: relative;
            width: 20px;
            height: 20px;
            background: linear-gradient(45deg, #ff3b30, #ff2d55);
            transform: rotate(-45deg);
            animation: beat 0.8s infinite alternate;
            box-shadow: 0 0 15px rgba(255, 59, 48, 0.6);
        }

        .heart-shape::before,
        .heart-shape::after {
            content: '';
            position: absolute;
            width: 20px;
            height: 20px;
            background: inherit;
            border-radius: 50%;
        }

        .heart-shape::before { top: -10px; left: 0; }
        .heart-shape::after { top: 0; left: 10px; }

        @keyframes fall {
            0% { transform: translateY(0) rotate(0deg) scale(1); opacity: 1; }
            100% { transform: translateY(110vh) rotate(360deg) scale(0.5); opacity: 0; }
        }

        @keyframes beat {
            0% { transform: rotate(-45deg) scale(1); }
            100% { transform: rotate(-45deg) scale(1.1); }
        }
    </style>
</head>
<body>
    <!-- Экран ввода -->
    <div class="input-screen" id="input-screen">
        <h2>Введи имя самой лучшей мамы в мире... ❤️</h2>
        <input type="text" id="nameInput" autocomplete="off">
        <button onclick="checkName()">Открыть</button>
    </div>

    <!-- Секретный контент -->
    <div class="secret-content" id="secret">
        <h1>С Днём Рождения, Мама!</h1>
        <h3>28 Ноября • Самый дорогой человек</h3>
        
        <p class="main-text">
            Мама, ты самая лучшая на всем белом свете! И да, я люблю тебя. Но не забываю и про мою вторую маму — это твоя мама. Я её тоже очень люблю. И, конечно же, я люблю твою сестру Sirin!<br><br>
            Но так как сегодня твой день рождения, я буду поздравлять тебя. Твои глаза как море: смотришь далеко-далеко, не можешь увидеть край. Море как будто не заканчивается, как и твои красивые глаза. А твой запах как у лилии — такой же нежный, как цветочек. Такая же красивая, как и ты.<br><br>
            Может, я не могу подарить тебе многое, но я могу подарить тебе вот это. Надеюсь, твое маленькое хрупкое сердце стало счастливее из-за моих слов. ❤️
        </p>
        
        <p class="thanks">
            Спасибо за твой нелёгкий труд врача и за то, что ты всегда рядом!
        </p>
    </div>

    <script>
        function checkName() {
            const input = document.getElementById("nameInput").value.toLowerCase().trim();
            const secretWord = "semsat"; // Имя мамы

            if (input === secretWord) {
                document.body.style.background = "radial-gradient(circle at center, #2a0a18 0%, #000000 100%)";
                
                const inputScreen = document.getElementById("input-screen");
                inputScreen.style.opacity = "0";
                setTimeout(() => { inputScreen.style.display = "none"; }, 800);

                const secret = document.getElementById("secret");
                secret.style.display = "block";
                setTimeout(() => { secret.style.opacity = "1"; }, 100);

                startHearts();
            } else {
                alert("Ой, это не то имя. Попробуй еще раз! 😉");
            }
        }

        document.getElementById("nameInput").addEventListener("keypress", function(event) {
            if (event.key === "Enter") {
                event.preventDefault();
                checkName();
            }
        });

        function startHearts() {
            setInterval(() => {
                const heartContainer = document.createElement("div");
                heartContainer.classList.add("heart");
                
                const heartShape = document.createElement("div");
                heartShape.classList.add("heart-shape");
                
                const scale = Math.random() * 0.8 + 0.4;
                heartShape.style.transform = `rotate(-45deg) scale(${scale})`;
                
                heartContainer.appendChild(heartShape);

                heartContainer.style.left = Math.random() * 100 + "vw";
                heartContainer.style.animationDuration = Math.random() * 3 + 3 + "s";

                document.body.appendChild(heartContainer);

                setTimeout(() => { heartContainer.remove(); }, 6000);
            }, 250);
        }
    </script>
</body>
</html>
"""

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(HTML_PAGE.encode("utf-8"))

if __name__ == "__main__":
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("0.0.0.0", PORT), MyHandler) as httpd:
        print(f"--- САЙТ ДЛЯ МАМЫ ЗАПУЩЕН ---")
        print(f"Открывай: http://192.168.1.102:{PORT}")
        httpd.serve_forever()