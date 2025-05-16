import transmission_rpc
import sys

# Transmission RPC 配置
RPC_HOST = '192.168.10.132'
RPC_PORT = 9091
RPC_USERNAME = 'admin'  # 如果没有认证，留空
RPC_PASSWORD = 'admin'

# 限速配置
DOWNLOAD_LIMIT = 0  # 单位：KB/s
UPLOAD_LIMIT = 10  # 单位：KB/s
TARGET_TRACKERS = [  # 目标Tracker白名单列表
    'm-team.cc', 'audiences.me', 'cinefiles.info', 'qingwa', 'ilovelemonhd.me'
    # 添加更多需要排除的Tracker...
]


def limit_speed_for_tracker(client):
    try:
        # 获取所有种子信息，包含 trackers 数据
        torrents = client.get_torrents(arguments=['id', 'trackers', 'uploadLimit', 'uploadLimited',])

        for torrent in torrents:
            trackers = [tracker.announce for tracker in torrent.trackers]
            # print(trackers)
            if not any(
                    any(tracker in url for tracker in TARGET_TRACKERS)
                    for url in trackers):

                if torrent.upload_limited and torrent.upload_limit == UPLOAD_LIMIT:
                    continue

                # 设置限速
                client.change_torrent(ids=torrent.id,
                                    downloadLimit=DOWNLOAD_LIMIT,
                                    downloadLimited=False,
                                    uploadLimit=UPLOAD_LIMIT,
                                    uploadLimited=True)
                print(
                    f'发现匹配种子 ID: {torrent.id}, hash: {torrent.hashString} 已应用限速设置'
                )

    except Exception as e:
        print(f'发生错误: {e}')


if __name__ == '__main__':
    mode = 0
    # 参数验证
    if len(sys.argv) != 2 or sys.argv[1] not in ('0', '1'):
        print("使用方法：")
        print("  限速模式：python script.py 1")
        print("  取消限速：python script.py 0")
        mode = 1

    try:
        # 连接Transmission
        client = transmission_rpc.Client(host=RPC_HOST,
                                         port=RPC_PORT,
                                         username=RPC_USERNAME,
                                         password=RPC_PASSWORD)

        if mode == 1 or sys.argv[1] == '1':
            # 执行Tracker限速
            limit_speed_for_tracker(client)

        else:
            # 取消所有限速
            client.change_torrent(ids=[t.id for t in client.get_torrents()],
                                  uploadLimited=False,
                                  downloadLimited=False,
                                  uploadLimit=0,
                                  downloadLimit=0)
            print("已移除所有种子的限速设置")


    except Exception as e:
        print(f"操作失败: {str(e)}")
        sys.exit(1)
