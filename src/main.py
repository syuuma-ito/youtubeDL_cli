from rich import print
from rich.progress import Progress
from yt_dlp import YoutubeDL


def choose_option(options):
    # 選択肢を表示し、選ぶプロンプトを出す
    # 選択肢になかったら、再帰
    def choose(option_len):
        user_ans = input(">>")

        if user_ans == "b":
            exit()

        try:
            user_ans = int(user_ans)
        except ValueError:
            print("[red]上の選択肢から選んでください[/]")
            return choose(option_len)

        if user_ans in range(option_len):
            return user_ans
        else:
            print("[red]上の選択肢から選んでください[/]")
            return choose(option_len)

    for i, option in enumerate(options):
        print(f"[green]{i}[/]:{option}")

    return choose(len(options))


video_opts_default = {
    "format": "best",
    "postprocessors": [
        {
            "key": "FFmpegVideoConvertor",
            "preferedformat": "mp4",
        }
    ],
    "quiet": True,
    # "outtmpl": f"{current_directory}%(title)s.%(ext)s",
}


mp3_opts_default = {
    "format": "bestaudio/best",
    "postprocessors": [
        {
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
        }
    ],
    "quiet": True,
    # "outtmpl": f"{current_directory}%(title)s.%(ext)s",
}


def download_video(url):
    # richで コンソールローディングを表示する
    with Progress() as progress:
        task = progress.add_task("[red]ダウンロード中...", total=100)

        def on_progress(d):
            if d["status"] == "downloading":
                progress.update(
                    task,
                    completed=int((d["total_bytes"] / d["downloaded_bytes"]) * 100),
                )
            if d["status"] == "finished":
                print("変換中...")

        video_opts_default["progress_hooks"] = [on_progress]

        with YoutubeDL(video_opts_default) as ydl:
            result = ydl.download([url])

            if result != 0:
                print("[red]ダウンロードに失敗しました[/]")
                exit(1)


def download_mp3(url):
    with YoutubeDL(mp3_opts_default) as ydl:
        result = ydl.download([url])

        if result != 0:
            print("[red]ダウンロードに失敗しました[/]")
            exit(1)


def main():
    res = choose_option(["動画をダウンロード", "mp3(音声のみ)をダウンロード", "終了"])
    if res == 0:
        # 動画をダウンロード
        url = input("ダウンロードしたい動画のURLを入力してください\n>>")
        print("動画をダウンロードしています...")
        try:
            download_video(url)
        except Exception as e:
            print("[red]ダウンロードに失敗しました[/]")
            return
        print("動画をダウンロードしました")
    elif res == 1:
        # mp3をダウンロード
        url = input("ダウンロードしたい動画のURLを入力してください\n>>")
        if url == "b":
            exit()
        print("mp3をダウンロードしています...")
        try:
            download_mp3(url)
        except Exception as e:
            print("[red]ダウンロードに失敗しました[/]")
            return
        print("mp3をダウンロードしました")
    elif res == 2:
        exit()


if __name__ == "__main__":
    while True:
        try:
            print("=====================================")
            main()
        except KeyboardInterrupt:
            exit()
